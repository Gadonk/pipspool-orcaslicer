# /// script
# dependencies = ["requests>=2.31,<3"]
# [tool.orcaslicer.plugin]
# name = "PipSpool"
# description = "Spoolman synchronization plugin for OrcaSlicer"
# author = "Donko"
# version = "2.0.0-dev"
# ///

"""PipSpool: synchronize Spoolman inventory into OrcaSlicer presets.

This implementation intentionally has no slicing-pipeline capability. Klipper
and Moonraker remain responsible for real-time Spoolman usage accounting.
"""

from __future__ import annotations

import json
import os
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import orca
import requests


# DEVELOPMENT DEFAULT ONLY. Restore localhost before a publishable release.
DEFAULT_SPOOLMAN_URL = "http://localhost:7912"
SETTINGS_FILENAME = "pipspool_settings.json"
LOG_FILENAME = "pipspool.log"
PROFILE_SUFFIX = " - PipSpool.json"
START_MARKER = "; PipSpool: begin managed spool ID"
END_MARKER = "; PipSpool: end managed spool ID"
LEGACY_START_MARKER = "; Spoolman Bridge: begin managed spool ID"
LEGACY_END_MARKER = "; Spoolman Bridge: end managed spool ID"

PLUGIN_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = PLUGIN_DIR / SETTINGS_FILENAME
LOG_PATH = PLUGIN_DIR / LOG_FILENAME


def log(message: str) -> None:
    try:
        with LOG_PATH.open("a", encoding="utf-8") as stream:
            stream.write(f"{message}\n")
    except OSError:
        return


def normalize_url(value: str) -> str:
    value = str(value or "").strip().rstrip("/")
    if not value:
        raise ValueError("Spoolman URL cannot be empty")
    if not value.startswith(("http://", "https://")):
        raise ValueError("Spoolman URL must begin with http:// or https://")
    return value


def load_settings() -> dict[str, Any]:
    settings: dict[str, Any] = {"spoolman_url": DEFAULT_SPOOLMAN_URL}
    try:
        stored = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        if isinstance(stored, dict):
            settings.update(stored)
    except (OSError, ValueError, TypeError):
        pass
    return settings


def save_settings(settings: dict[str, Any]) -> None:
    payload = dict(settings)
    payload["spoolman_url"] = normalize_url(payload.get("spoolman_url", ""))
    temporary = SETTINGS_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, SETTINGS_PATH)


def safe_filename(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "", str(value)).strip()
    return cleaned or "Unnamed spool"


def spool_id_from_name(filename: str) -> int | None:
    match = re.search(r"\(#(\d+)\)", filename)
    return int(match.group(1)) if match else None


def managed_start_gcode(existing: Any, spool_id: int) -> list[str]:
    if isinstance(existing, list):
        text = str(existing[0]) if existing else ""
    else:
        text = "" if existing is None else str(existing)

    for begin, end in (
        (START_MARKER, END_MARKER),
        (LEGACY_START_MARKER, LEGACY_END_MARKER),
    ):
        pattern = re.compile(
            rf"(?:\r?\n)?{re.escape(begin)}.*?{re.escape(end)}(?:\r?\n)?",
            re.DOTALL,
        )
        text = pattern.sub("\n", text)

    preserved = text.rstrip()
    block = f"{START_MARKER}\nSET_SPOOL_ID ID={int(spool_id)}\n{END_MARKER}"
    return [f"{preserved}\n\n{block}" if preserved else block]


def support_directory() -> Path | None:
    for parent in (PLUGIN_DIR, *PLUGIN_DIR.parents):
        if parent.name == "OrcaSlicer":
            return parent

    appdata = os.environ.get("APPDATA")
    candidates = [
        Path.home() / "Library" / "Application Support" / "OrcaSlicer",
        Path.home() / ".config" / "OrcaSlicer",
    ]
    if appdata:
        candidates.append(Path(appdata) / "OrcaSlicer")
    return next((path for path in candidates if path.is_dir()), None)


@dataclass
class SyncReport:
    active_spools: int = 0
    created: int = 0
    updated: int = 0
    renamed: int = 0
    removed: int = 0
    unchanged: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.created or self.updated or self.renamed or self.removed)

    def summary(self) -> str:
        details = (
            f"Active spools: {self.active_spools}\n"
            f"Created: {self.created}\nUpdated: {self.updated}\n"
            f"Renamed: {self.renamed}\nRemoved: {self.removed}\n"
            f"Unchanged: {self.unchanged}"
        )
        if self.errors:
            details += f"\nErrors: {len(self.errors)}\n" + "\n".join(self.errors[:5])
        return details


class SpoolmanClient:
    def __init__(self, base_url: str):
        self.base_url = normalize_url(base_url)

    def active_spools(self) -> list[dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/spool",
            params={"allow_archived": "false"},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("Spoolman returned an unexpected spool response")
        return [item for item in payload if isinstance(item, dict)]


class OrcaProfiles:
    def __init__(self, root: Path):
        self.root = root
        self.user_root = root / "user"
        self.system_root = root / "system"
        self.system_presets = self._system_preset_index()

    def _system_preset_index(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        if not self.system_root.is_dir():
            return result
        for path in self.system_root.rglob("*.json"):
            if "filament" not in path.parts:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                name = data.get("name")
                if isinstance(name, str) and name:
                    result[name] = data
            except (OSError, ValueError, TypeError):
                continue
        return result

    def user_filament_directories(self) -> list[Path]:
        if not self.user_root.is_dir():
            return []
        directories = []
        for profile_root in self.user_root.iterdir():
            if profile_root.is_dir():
                directories.append(profile_root / "filament")
        return directories

    def parent_for(self, vendor: str, material: str) -> str:
        material_key = material.casefold()
        vendor_key = vendor.casefold()
        for name in self.system_presets:
            folded = name.casefold()
            if vendor_key in folded and material_key in folded:
                return name
        for name in self.system_presets:
            if f"generic {material_key}" in name.casefold():
                return name
        return f"Generic {material} @System"

    def inherited_start_gcode(self, preset: dict[str, Any]) -> Any:
        visited: set[str] = set()
        parent_name = preset.get("inherits")
        while isinstance(parent_name, str) and parent_name and parent_name not in visited:
            visited.add(parent_name)
            parent = self.system_presets.get(parent_name)
            if not parent:
                break
            if "filament_start_gcode" in parent:
                return parent["filament_start_gcode"]
            parent_name = parent.get("inherits")
        return []


def filament_material(filament: dict[str, Any]) -> str:
    raw = str(filament.get("material") or "PLA").upper()
    for known in ("PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC", "PVA"):
        if known in raw:
            return known
    return raw


def numeric(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def desired_preset(
    spool: dict[str, Any],
    existing: dict[str, Any],
    profiles: OrcaProfiles,
) -> tuple[str, dict[str, Any]]:
    spool_id = int(spool["id"])
    filament = spool.get("filament") or {}
    vendor_data = filament.get("vendor") or {}
    vendor = str(vendor_data.get("name") or "Generic").strip()
    filament_name = str(filament.get("name") or filament_material(filament)).strip()
    material = filament_material(filament)
    display_name = f"{vendor} {filament_name} (#{spool_id}) - PipSpool"

    preset = dict(existing)
    if not preset:
        preset["inherits"] = profiles.parent_for(vendor, material)

    start_gcode = preset.get("filament_start_gcode")
    if start_gcode is None:
        start_gcode = profiles.inherited_start_gcode(preset)

    color = str(filament.get("color_hex") or "FFFFFF").lstrip("#")
    preset.update(
        {
            "name": display_name,
            "from": "User",
            "version": "2.5.0.0",
            "filament_settings_id": [display_name],
            "filament_vendor": [vendor],
            "filament_type": [material],
            "default_filament_colour": [f"#{color}"],
            "filament_start_gcode": managed_start_gcode(start_gcode, spool_id),
        }
    )

    nozzle = numeric(filament.get("extruder_temp"))
    if nozzle and nozzle > 0:
        temperature = str(round(nozzle))
        preset["nozzle_temperature"] = [temperature]
        preset["nozzle_temperature_initial_layer"] = [temperature]

    bed = numeric(filament.get("bed_temp"))
    if bed and bed > 0:
        temperature = str(round(bed))
        preset["bed_temperature"] = [temperature]
        preset["bed_temperature_initial_layer"] = [temperature]

    price = numeric(spool.get("price"))
    if price is None:
        price = numeric(filament.get("price"))
    weight = numeric(filament.get("weight"))
    if price is not None and weight and weight > 0:
        preset["filament_cost"] = [f"{price * 1000 / weight:.2f}"]

    extras = dict(filament.get("extra") or {})
    extras.update(spool.get("extra") or {})
    max_flow = numeric(extras.get("max_volumetric_speed"))
    if max_flow is not None and max_flow > 0:
        preset["filament_max_volumetric_speed"] = [str(max_flow)]

    return display_name, preset


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def sync_profiles(spools: list[dict[str, Any]], profiles: OrcaProfiles) -> SyncReport:
    report = SyncReport(active_spools=len(spools))
    active_ids = {int(spool["id"]) for spool in spools if spool.get("id") is not None}

    for directory in profiles.user_filament_directories():
        directory.mkdir(parents=True, exist_ok=True)
        files_by_id: dict[int, list[Path]] = {}
        for path in directory.glob("*.json"):
            spool_id = spool_id_from_name(path.name)
            if spool_id is not None and path.name.endswith((PROFILE_SUFFIX, " - Spoolman.json")):
                files_by_id.setdefault(spool_id, []).append(path)

        for spool in spools:
            try:
                spool_id = int(spool["id"])
                candidates = sorted(files_by_id.get(spool_id, []))
                source = candidates[0] if candidates else None
                existing = read_json(source) if source else {}
                display_name, data = desired_preset(spool, existing, profiles)
                target = directory / f"{safe_filename(display_name)}.json"

                if source is None:
                    write_json_atomic(target, data)
                    report.created += 1
                elif source != target:
                    write_json_atomic(target, data)
                    for old_path in candidates:
                        if old_path != target and old_path.exists():
                            old_path.unlink()
                    report.renamed += 1
                elif existing != data:
                    write_json_atomic(target, data)
                    for duplicate in candidates[1:]:
                        if duplicate.exists():
                            duplicate.unlink()
                    report.updated += 1
                else:
                    report.unchanged += 1
            except Exception as exc:
                report.errors.append(f"Spool {spool.get('id', '?')}: {exc}")

        for spool_id, paths in files_by_id.items():
            if spool_id in active_ids:
                continue
            for path in paths:
                try:
                    path.unlink()
                    report.removed += 1
                except OSError as exc:
                    report.errors.append(f"Remove {path.name}: {exc}")

    return report


LEGACY_PLUGIN_REFS = {
    "spoolman_bridge;;Filament Usage Updater",
    "Spoolman Bridge;3ad590dc-6698-4327-9005-12b977229ed2;Filament Usage Updater",
}


def remove_legacy_pipeline_artifacts(profiles: OrcaProfiles) -> tuple[int, int]:
    removed_processes = 0
    cleaned_presets = 0
    if not profiles.user_root.is_dir():
        return removed_processes, cleaned_presets

    for path in profiles.user_root.rglob("*.json"):
        if path.parent.name == "process" and path.name.endswith(" - SpoolMan.json"):
            path.unlink()
            removed_processes += 1
            continue

        data = read_json(path)
        changed = False
        refs = data.get("plugins")
        if isinstance(refs, list):
            filtered = [ref for ref in refs if ref not in LEGACY_PLUGIN_REFS]
            if filtered != refs:
                changed = True
                if filtered:
                    data["plugins"] = filtered
                else:
                    data.pop("plugins", None)
        elif refs in LEGACY_PLUGIN_REFS:
            data.pop("plugins", None)
            changed = True

        pipeline = data.get("slicing_pipeline_plugin")
        if isinstance(pipeline, list):
            filtered = [name for name in pipeline if name != "Filament Usage Updater"]
            if filtered != pipeline:
                changed = True
                if filtered:
                    data["slicing_pipeline_plugin"] = filtered
                else:
                    data.pop("slicing_pipeline_plugin", None)
        elif pipeline == "Filament Usage Updater":
            data.pop("slicing_pipeline_plugin", None)
            changed = True

        if changed:
            write_json_atomic(path, data)
            cleaned_presets += 1

    return removed_processes, cleaned_presets


def orca_profiles() -> OrcaProfiles:
    root = support_directory()
    if root is None:
        raise RuntimeError("OrcaSlicer profile directory could not be found")
    return OrcaProfiles(root)


def show_message(message: str, title: str = "PipSpool", icon: str = "info") -> None:
    orca.host.ui.message(message, title=title, icon=icon)


class SyncCapability(orca.script.ScriptPluginCapabilityBase):
    def get_name(self):
        return "Sync Spoolman Profiles"

    def execute(self):
        def work():
            try:
                settings = load_settings()
                spools = SpoolmanClient(settings["spoolman_url"]).active_spools()
                report = sync_profiles(spools, orca_profiles())
                log(f"[SYNC] {report.summary().replace(chr(10), '; ')}")
                suffix = "\n\nRestart OrcaSlicer to load changed presets." if report.changed else ""
                show_message(report.summary() + suffix, icon="warning" if report.errors else "info")
            except Exception as exc:
                log(f"[SYNC ERROR] {exc}")
                show_message(f"Synchronization failed:\n{exc}", icon="error")

        threading.Thread(target=work, daemon=True).start()
        return orca.ExecutionResult.success("PipSpool synchronization started")


class LegacyCleanupCapability(orca.script.ScriptPluginCapabilityBase):
    def get_name(self):
        return "Remove Legacy Double Profiles"

    def execute(self):
        try:
            removed, cleaned = remove_legacy_pipeline_artifacts(orca_profiles())
            message = (
                f"Removed {removed} legacy process profile(s).\n"
                f"Cleaned {cleaned} legacy preset reference(s).\n\n"
                "Synced PipSpool filament presets were preserved. Restart OrcaSlicer."
            )
            show_message(message)
            return orca.ExecutionResult.success(message)
        except Exception as exc:
            return orca.ExecutionResult.failure(
                orca.PluginResult.RecoverableError,
                f"Legacy cleanup failed: {exc}",
            )


class SettingsCapability(orca.script.ScriptPluginCapabilityBase):
    def get_name(self):
        return "PipSpool Settings"

    def execute(self):
        current_url = load_settings().get("spoolman_url", DEFAULT_SPOOLMAN_URL)
        html = f"""<!doctype html>
<html><head><style>
body {{ background:#202124; color:#f1f3f4; font-family:system-ui,sans-serif; padding:24px; }}
h2 {{ color:#36d7e8; }} label {{ display:block; margin-bottom:8px; }}
input {{ width:100%; box-sizing:border-box; padding:10px; color:#fff; background:#303134; border:1px solid #5f6368; border-radius:6px; }}
.buttons {{ display:flex; justify-content:flex-end; gap:10px; margin-top:22px; }}
button {{ padding:9px 15px; border:0; border-radius:6px; cursor:pointer; }}
.primary {{ background:#28a9bc; color:white; }}
</style></head><body>
<h2>PipSpool</h2>
<p>Spoolman synchronization plugin for OrcaSlicer</p>
<label for="url">Spoolman server URL</label>
<input id="url" value="{current_url}" placeholder="{DEFAULT_SPOOLMAN_URL}">
<div class="buttons"><button onclick="window.orca.postMessage({{action:'cancel'}})">Cancel</button>
<button class="primary" onclick="window.orca.postMessage({{action:'save',url:document.getElementById('url').value}})">Save</button></div>
</body></html>"""

        def on_message(data):
            if not isinstance(data, dict):
                return
            if data.get("action") == "cancel":
                window.close()
                return
            if data.get("action") == "save":
                try:
                    save_settings({"spoolman_url": data.get("url", "")})
                    window.close()
                    show_message("PipSpool settings saved.")
                except Exception as exc:
                    show_message(str(exc), icon="error")

        window = orca.host.ui.create_window(
            html=html,
            title="PipSpool Settings",
            on_message=on_message,
        )
        return orca.ExecutionResult.success("PipSpool settings opened")


@orca.plugin
class PipSpoolPlugin(orca.base):
    def register_capabilities(self):
        orca.register_capability(SyncCapability)
        orca.register_capability(LegacyCleanupCapability)
        orca.register_capability(SettingsCapability)
