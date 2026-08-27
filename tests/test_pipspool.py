import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


def load_plugin_module():
    orca = types.ModuleType("orca")
    orca.script = types.SimpleNamespace(ScriptPluginCapabilityBase=object)
    orca.base = object
    orca.plugin = lambda cls: cls
    orca.register_capability = lambda cls: None
    orca.host = types.SimpleNamespace(ui=types.SimpleNamespace())
    orca.ExecutionResult = types.SimpleNamespace(success=lambda message="": message)
    orca.PluginResult = types.SimpleNamespace(RecoverableError="recoverable")
    sys.modules["orca"] = orca

    requests = types.ModuleType("requests")
    requests.get = Mock()
    requests.post = Mock()
    sys.modules["requests"] = requests

    path = Path(__file__).parents[1] / "pipspool_v2_0_8_win_x86_64.py"
    spec = importlib.util.spec_from_file_location("pipspool_v2_dev", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pipspool = load_plugin_module()


class ManagedGCodeTests(unittest.TestCase):
    def test_preserves_custom_gcode_and_replaces_legacy_block(self):
        existing = [
            "M900 K0.04\n\n"
            "; Spoolman Bridge: begin managed spool ID\n"
            "SET_SPOOL_ID ID=8\n"
            "; Spoolman Bridge: end managed spool ID"
        ]
        result = pipspool.managed_start_gcode(existing, 42)[0]
        self.assertIn("M900 K0.04", result)
        self.assertIn("SET_SPOOL_ID ID=42", result)
        self.assertNotIn("ID=8", result)
        self.assertEqual(result.count(pipspool.START_MARKER), 1)

    def test_spoolman_custom_gcode_replaces_only_managed_block(self):
        existing = [
            "M900 K0.04\n\n"
            f"{pipspool.START_MARKER}\n"
            "SET_SPOOL_ID ID=8\n"
            f"{pipspool.END_MARKER}"
        ]
        encoded = json.dumps("M117 Loading spool 42\nSET_ACTIVE_SPOOL ID=42")
        result = pipspool.managed_start_gcode(existing, 42, encoded)[0]

        self.assertIn("M900 K0.04", result)
        self.assertIn("M117 Loading spool 42", result)
        self.assertIn("SET_ACTIVE_SPOOL ID=42", result)
        self.assertNotIn("SET_SPOOL_ID ID=8", result)

    def test_blank_custom_gcode_keeps_automatic_spool_id(self):
        result = pipspool.managed_start_gcode([], 42, json.dumps(""))[0]
        self.assertIn("SET_SPOOL_ID ID=42", result)

    def test_double_encoded_spoolman_text_is_decoded(self):
        encoded = json.dumps(json.dumps("M117 Ready"))
        self.assertEqual(pipspool.decode_extra_value(encoded), "M117 Ready")


class SpoolmanClientTests(unittest.TestCase):
    def test_creates_missing_spool_start_gcode_field(self):
        get_response = Mock()
        get_response.json.return_value = []
        post_response = Mock()
        with (
            patch.object(pipspool.requests, "get", return_value=get_response),
            patch.object(pipspool.requests, "post", return_value=post_response) as post,
        ):
            created = pipspool.SpoolmanClient("http://spoolman.test").ensure_start_gcode_field()

        self.assertTrue(created)
        get_response.raise_for_status.assert_called_once_with()
        post_response.raise_for_status.assert_called_once_with()
        post.assert_called_once_with(
            "http://spoolman.test/api/v1/field/spool/start_gcode",
            json={"name": "Start G-code", "field_type": "text", "order": 0},
            timeout=10,
        )

    def test_keeps_existing_text_field_without_posting(self):
        get_response = Mock()
        get_response.json.return_value = [{"key": "start_gcode", "field_type": "text"}]
        with (
            patch.object(pipspool.requests, "get", return_value=get_response),
            patch.object(pipspool.requests, "post") as post,
        ):
            created = pipspool.SpoolmanClient("http://spoolman.test").ensure_start_gcode_field()

        self.assertFalse(created)
        post.assert_not_called()


class SynchronizationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        (root / "system").mkdir()
        self.filament_dir = root / "user" / "default" / "filament"
        self.filament_dir.mkdir(parents=True)
        self.profiles = pipspool.OrcaProfiles(root)

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def spool(name="PLA Basic", color="123ABC"):
        return {
            "id": 42,
            "price": 20,
            "filament": {
                "name": name,
                "material": "PLA",
                "color_hex": color,
                "weight": 1000,
                "settings_extruder_temp": 218,
                "settings_bed_temp": 57,
                "vendor": {"name": "Example"},
            },
        }

    def test_renames_same_id_and_preserves_orca_overrides(self):
        old_path = self.filament_dir / "Example Old Name (#42) - Spoolman.json"
        old_path.write_text(
            json.dumps(
                {
                    "name": "Example Old Name (#42) - Spoolman",
                    "inherits": "Generic PLA @System",
                    "filament_flow_ratio": ["0.97"],
                }
            ),
            encoding="utf-8",
        )

        report = pipspool.sync_profiles([self.spool()], self.profiles)
        target = self.filament_dir / "(#42) PLA Basic - Example - PipSpool.json"

        self.assertTrue(target.exists())
        self.assertFalse(old_path.exists())
        data = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(data["filament_flow_ratio"], ["0.97"])
        self.assertIn("SET_SPOOL_ID ID=42", data["filament_start_gcode"][0])
        self.assertEqual(report.renamed, 1)

    def test_updates_existing_same_id_without_duplicate(self):
        pipspool.sync_profiles([self.spool()], self.profiles)
        report = pipspool.sync_profiles([self.spool(color="FFFFFF")], self.profiles)
        files = list(self.filament_dir.glob("*(#42)*.json"))
        self.assertEqual(len(files), 1)
        data = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(data["default_filament_colour"], ["#FFFFFF"])
        self.assertEqual(report.updated, 1)

    def test_uses_spoolman_temperatures_for_nozzle_and_every_bed_type(self):
        pipspool.sync_profiles([self.spool()], self.profiles)
        path = next(self.filament_dir.glob("*.json"))
        data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(data["nozzle_temperature"], ["218"])
        self.assertEqual(data["nozzle_temperature_initial_layer"], ["218"])
        for plate_key in (
            "supertack_plate_temp",
            "cool_plate_temp",
            "textured_cool_plate_temp",
            "eng_plate_temp",
            "hot_plate_temp",
            "textured_plate_temp",
        ):
            self.assertEqual(data[plate_key], ["57"])
            self.assertEqual(data[f"{plate_key}_initial_layer"], ["57"])

    def test_removes_inactive_generated_profile(self):
        pipspool.sync_profiles([self.spool()], self.profiles)
        report = pipspool.sync_profiles([], self.profiles)
        self.assertEqual(list(self.filament_dir.glob("*.json")), [])
        self.assertEqual(report.removed, 1)

    def test_archived_spool_is_removed_from_orca(self):
        pipspool.sync_profiles([self.spool()], self.profiles)
        archived = self.spool()
        archived["archived"] = True

        report = pipspool.sync_profiles([archived], self.profiles)

        self.assertEqual(list(self.filament_dir.glob("*.json")), [])
        self.assertEqual(report.active_spools, 0)
        self.assertEqual(report.removed, 1)

    def test_profile_name_starts_with_spool_id_for_sorting(self):
        pipspool.sync_profiles([self.spool()], self.profiles)
        path = next(self.filament_dir.glob("*.json"))
        data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(path.name, "(#42) PLA Basic - Example - PipSpool.json")
        self.assertEqual(data["name"], "(#42) PLA Basic - Example - PipSpool")

    def test_syncs_spool_level_custom_start_gcode(self):
        spool = self.spool()
        spool["extra"] = {
            "start_gcode": json.dumps("M117 Custom spool\nSET_ACTIVE_SPOOL ID=42")
        }
        pipspool.sync_profiles([spool], self.profiles)
        data = json.loads(next(self.filament_dir.glob("*.json")).read_text(encoding="utf-8"))
        start_gcode = data["filament_start_gcode"][0]

        self.assertIn("M117 Custom spool", start_gcode)
        self.assertIn("SET_ACTIVE_SPOOL ID=42", start_gcode)


class ArchitectureTests(unittest.TestCase):
    def test_only_intended_capabilities_are_registered(self):
        source = (Path(__file__).parents[1] / "pipspool_v2_0_8_win_x86_64.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("SlicingPipelineCapabilityBase", source)
        self.assertNotIn("/use", source)
        self.assertNotIn("requests.put", source)
        self.assertEqual(source.count("orca.register_capability("), 3)

    def test_settings_ui_has_clear_actions(self):
        source = (Path(__file__).parents[1] / "pipspool_v2_0_8_win_x86_64.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("Test connection", source)
        self.assertIn("Save settings", source)
        self.assertIn("safe_current_url", source)
        self.assertIn("data:image/webp;base64,", source)
        self.assertIn('class="logo"', source)

    def test_settings_open_on_first_load_without_saved_settings(self):
        capability = pipspool.SettingsCapability()
        opened = []
        capability._open_settings_window = lambda: opened.append(True)
        with patch.object(pipspool, "has_saved_settings", return_value=False):
            capability.on_load()
        self.assertEqual(opened, [True])

    def test_settings_stay_closed_when_configuration_is_saved(self):
        capability = pipspool.SettingsCapability()
        opened = []
        capability._open_settings_window = lambda: opened.append(True)
        with patch.object(pipspool, "has_saved_settings", return_value=True):
            capability.on_load()
        self.assertEqual(opened, [])


if __name__ == "__main__":
    unittest.main()
