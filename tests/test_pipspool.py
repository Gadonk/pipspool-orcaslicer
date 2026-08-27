import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


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

    path = Path(__file__).parents[1] / "pipspool_v2_0_0_dev.py"
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
        target = self.filament_dir / "Example PLA Basic (#42) - PipSpool.json"

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

    def test_removes_inactive_generated_profile(self):
        pipspool.sync_profiles([self.spool()], self.profiles)
        report = pipspool.sync_profiles([], self.profiles)
        self.assertEqual(list(self.filament_dir.glob("*.json")), [])
        self.assertEqual(report.removed, 1)


class ArchitectureTests(unittest.TestCase):
    def test_only_intended_capabilities_are_registered(self):
        source = (Path(__file__).parents[1] / "pipspool_v2_0_0_dev.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("SlicingPipelineCapabilityBase", source)
        self.assertNotIn("/use", source)
        self.assertNotIn("requests.put", source)
        self.assertEqual(source.count("orca.register_capability("), 3)


if __name__ == "__main__":
    unittest.main()
