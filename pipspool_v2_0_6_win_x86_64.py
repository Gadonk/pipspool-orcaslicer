# /// script
# dependencies = ["requests"]
# [tool.orcaslicer.plugin]
# name = "PipSpool"
# description = "Spoolman synchronization plugin for OrcaSlicer"
# author = "Donko"
# version = "2.0.6"
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
from html import escape
from pathlib import Path
from typing import Any

import orca
import requests


# Public default. Configure the Spoolman server address in PipSpool Settings.
DEFAULT_SPOOLMAN_URL = "http://localhost:7912"
SETTINGS_FILENAME = "pipspool_settings.json"
LOG_FILENAME = "pipspool.log"
PROFILE_SUFFIX = " - PipSpool.json"
START_MARKER = "; PipSpool: begin managed spool ID"
END_MARKER = "; PipSpool: end managed spool ID"
LEGACY_START_MARKER = "; Spoolman Bridge: begin managed spool ID"
LEGACY_END_MARKER = "; Spoolman Bridge: end managed spool ID"
PIPSPOOL_LOGO_DATA_URI = (
    "data:image/webp;base64,"
    "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"
)

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
        return [
            item
            for item in payload
            if isinstance(item, dict) and not spool_is_archived(item)
        ]


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


def spool_is_archived(spool: dict[str, Any]) -> bool:
    value = spool.get("archived", False)
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes", "on"}
    return bool(value)


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
    display_name = f"(#{spool_id}) {vendor} {filament_name} - PipSpool"

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

    nozzle = numeric(filament.get("settings_extruder_temp"))
    if nozzle and nozzle > 0:
        temperature = str(round(nozzle))
        preset["nozzle_temperature"] = [temperature]
        preset["nozzle_temperature_initial_layer"] = [temperature]

    bed = numeric(filament.get("settings_bed_temp"))
    if bed and bed > 0:
        temperature = str(round(bed))
        for plate_key in (
            "supertack_plate_temp",
            "cool_plate_temp",
            "textured_cool_plate_temp",
            "eng_plate_temp",
            "hot_plate_temp",
            "textured_plate_temp",
        ):
            preset[plate_key] = [temperature]
            preset[f"{plate_key}_initial_layer"] = [temperature]

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
    spools = [spool for spool in spools if not spool_is_archived(spool)]
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

    def on_load(self):
        self._open_settings_window()

    def execute(self):
        self._open_settings_window()
        return orca.ExecutionResult.success("PipSpool settings opened")

    def _open_settings_window(self):
        current_url = load_settings().get("spoolman_url", DEFAULT_SPOOLMAN_URL)
        safe_current_url = escape(str(current_url), quote=True)
        safe_default_url = escape(DEFAULT_SPOOLMAN_URL, quote=True)
        html = f"""<!doctype html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root {{ color-scheme:dark; --page:#202124; --panel:#292a2d; --field:#1f2022;
  --line:#55585d; --text:#f1f3f4; --muted:#aeb4ba; --accent:#37c9da;
  --accent-hover:#51d6e5; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:28px; background:var(--page); color:var(--text);
  font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif; }}
.header {{ display:flex; align-items:center; gap:16px; margin-bottom:20px; }}
.logo {{ width:64px; height:64px; flex:0 0 64px; object-fit:contain;
  filter:drop-shadow(0 4px 8px rgba(0,0,0,.28)); }}
h1 {{ margin:0; font-size:21px; line-height:1.15; }}
.subtitle {{ margin:4px 0 0; color:var(--muted); font-size:13px; }}
.card {{ padding:20px; border:1px solid #3d3f43; border-radius:12px; background:var(--panel); }}
.card-title {{ margin:0 0 5px; font-size:15px; font-weight:650; }}
.help {{ margin:0 0 17px; color:var(--muted); }}
label {{ display:block; margin-bottom:7px; font-weight:600; }}
input {{ width:100%; padding:11px 12px; border:1px solid var(--line); border-radius:7px;
  outline:none; background:var(--field); color:var(--text); font:inherit; }}
input:focus {{ border-color:var(--accent); box-shadow:0 0 0 2px rgba(55,201,218,.18); }}
.example {{ margin-top:7px; color:var(--muted); font-size:12px; }}
.actions {{ display:flex; align-items:center; justify-content:space-between; gap:10px; margin-top:22px; }}
.right {{ display:flex; gap:9px; }}
button {{ min-height:36px; padding:8px 14px; border:1px solid var(--line); border-radius:7px;
  cursor:pointer; background:transparent; color:var(--text); font:600 13px system-ui,sans-serif; }}
button:hover {{ background:rgba(255,255,255,.06); }}
.primary {{ border-color:var(--accent); background:var(--accent); color:#102326; }}
.primary:hover {{ background:var(--accent-hover); }}
</style></head><body>
<div class="header"><img class="logo" src="{PIPSPOOL_LOGO_DATA_URI}" alt="PipSpool logo"><div><h1>PipSpool settings</h1>
<p class="subtitle">Connect OrcaSlicer to your Spoolman server</p></div></div>
<div class="card"><p class="card-title">Spoolman connection</p>
<p class="help">Enter the address you normally use to open Spoolman.</p>
<label for="url">Server address</label>
<input id="url" type="url" spellcheck="false" autocomplete="off"
 value="{safe_current_url}" placeholder="{safe_default_url}">
<div class="example">Include http:// or https:// and the port, if one is used.</div></div>
<div class="actions"><button onclick="send('test')">Test connection</button>
<div class="right"><button onclick="send('cancel')">Cancel</button>
<button class="primary" onclick="send('save')">Save settings</button></div></div>
<script>
const url = document.getElementById('url');
function send(action) {{ window.orca.postMessage({{action:action,url:url.value}}); }}
url.addEventListener('keydown', event => {{ if (event.key === 'Enter') send('save'); }});
</script>
</body></html>"""

        def on_message(data):
            if not isinstance(data, dict):
                return
            if data.get("action") == "cancel":
                window.close()
                return
            if data.get("action") == "test":
                try:
                    test_url = normalize_url(data.get("url", ""))
                except Exception as exc:
                    show_message(str(exc), title="Connection test", icon="error")
                    return

                def test_connection():
                    try:
                        spools = SpoolmanClient(test_url).active_spools()
                        show_message(
                            f"Connection successful.\n\nSpoolman returned {len(spools)} active spool(s).",
                            title="Connection test",
                        )
                    except Exception as exc:
                        log(f"[CONNECTION TEST ERROR] {exc}")
                        show_message(
                            f"Could not connect to Spoolman.\n\n{exc}",
                            title="Connection test",
                            icon="error",
                        )

                threading.Thread(target=test_connection, daemon=True).start()
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


@orca.plugin
class PipSpoolPlugin(orca.base):
    def register_capabilities(self):
        orca.register_capability(SyncCapability)
        orca.register_capability(LegacyCleanupCapability)
        orca.register_capability(SettingsCapability)
