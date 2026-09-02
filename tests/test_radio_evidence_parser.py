from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "analyze_radio_evidence.py"


class RadioEvidenceParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("radio_evidence", TOOL)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {TOOL}")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_scans_relevant_radio_properties(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "build.prop").write_text(
                "ro.vendor.product.name=HydrogenONE\n"
                "persist.vendor.radio.multisim.config=dsds\n"
                "ro.telephony.default_network=9\n"
                "unrelated.key=value\n",
                encoding="utf-8",
            )
            rows = self.module.scan_property_files(root)
            keys = {row["key"] for row in rows}
            self.assertIn("persist.vendor.radio.multisim.config", keys)
            self.assertIn("ro.telephony.default_network", keys)
            self.assertNotIn("unrelated.key", keys)

    def test_scans_qcrild_service_and_explicit_start_trigger(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_dir = root / "etc" / "init"
            init_dir.mkdir(parents=True)
            (init_dir / "qcrild.rc").write_text(
                "service vendor.qcrild /vendor/bin/hw/qcrild\n"
                "    class main\n"
                "    disabled\n\n"
                "service vendor.qcrild2 /vendor/bin/hw/qcrild -c 2\n"
                "    class main\n"
                "    disabled\n",
                encoding="utf-8",
            )
            (init_dir / "init.qcom.rc").write_text(
                "on boot\n"
                "    start vendor.qcrild\n",
                encoding="utf-8",
            )
            result = self.module.scan_init_files(root)
            services = {row["name"]: row for row in result["services"]}
            self.assertTrue(services["vendor.qcrild"]["disabled"])
            self.assertTrue(services["vendor.qcrild2"]["disabled"])
            self.assertIn("vendor.qcrild", {row["target"] for row in result["starts"]})
            self.assertNotIn("vendor.qcrild2", {row["target"] for row in result["starts"]})

    def test_summary_does_not_invent_extra_ril_instances(self) -> None:
        evidence = {
            "properties": [
                {"key": "persist.vendor.radio.multisim.config", "value": "ssss", "path": "build.prop", "line": 1}
            ],
            "init": {
                "services": [
                    {"name": "vendor.qcrild", "executable": "/vendor/bin/hw/qcrild", "disabled": True},
                    {"name": "vendor.qcrild2", "executable": "/vendor/bin/hw/qcrild -c 2", "disabled": True},
                ],
                "starts": [{"target": "vendor.qcrild", "trigger": "boot", "path": "init.qcom.rc", "line": 10}],
                "stops": [],
                "imports": [],
            },
        }
        summary = self.module.derive_summary(evidence)
        self.assertEqual(summary["explicit_qcrild_start_targets"], ["vendor.qcrild"])
        self.assertEqual(summary["multisim_values"], ["ssss"])
        self.assertEqual(summary["recommended_runtime_instances_from_evidence"], ["vendor.qcrild"])


if __name__ == "__main__":
    unittest.main()
