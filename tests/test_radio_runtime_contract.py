from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INIT_QCOM = ROOT / "rootdir" / "etc" / "init" / "hw" / "init.qcom.rc"
SHELL_EVIDENCE = ROOT / "docs" / "stock" / "h1a1000-r118" / "radio-shell-evidence.json"
LAYER_EVIDENCE = ROOT / "docs" / "stock" / "h1a1000-r118" / "radio-all-layers-evidence.json"


class Red118RadioRuntimeContractTest(unittest.TestCase):
    def test_stock_authority_requires_qcrild_dsds_path(self) -> None:
        shell = json.loads(SHELL_EVIDENCE.read_text(encoding="utf-8"))
        layers = json.loads(LAYER_EVIDENCE.read_text(encoding="utf-8"))

        self.assertEqual(layers["summary"]["multisim_values"], ["dsds"])
        tokens = shell["ver_info"]["mpss_tokens"]
        self.assertTrue(any(token.startswith("MPSS.AT.") for token in tokens), tokens)

        targets = {row["target"] for row in shell["radio_shell_controls"] if row["verb"] == "start"}
        self.assertIn("vendor.qcrild", targets)
        self.assertIn("vendor.qcrild2", targets)

    def test_android15_rootdir_starts_primary_and_dsds_qcrild(self) -> None:
        text = INIT_QCOM.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^\s*start vendor\.qcrild\s*$")
        self.assertRegex(text, r"(?m)^\s*start vendor\.qcrild2\s*$")

    def test_android15_rootdir_does_not_start_tsts_or_legacy_rild(self) -> None:
        text = INIT_QCOM.read_text(encoding="utf-8")
        forbidden = (
            "vendor.qcrild3",
            "vendor.ril-daemon",
            "vendor.ril-daemon2",
            "vendor.ril-daemon3",
            "ril-daemon",
        )
        for service in forbidden:
            self.assertNotRegex(text, rf"(?m)^\s*start\s+{re.escape(service)}\s*$", service)


if __name__ == "__main__":
    unittest.main()
