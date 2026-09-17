from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVICE_MK = ROOT / "device.mk"
VENDOR_PROP = ROOT / "vendor.prop"


class RadioDataPlaneRuntimeContractTest(unittest.TestCase):
    def test_red118_dsds_defaults_to_lte_capable_mode(self) -> None:
        text = VENDOR_PROP.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^ro\.telephony\.default_network=22,22$")

    def test_fp3_data_plane_is_enabled(self) -> None:
        text = VENDOR_PROP.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^persist\.vendor\.dpmhalservice\.enable=1$")
        self.assertRegex(text, r"(?m)^persist\.vendor\.data\.mode=concurrent$")
        self.assertRegex(text, r"(?m)^ro\.vendor\.use_data_netmgrd=true$")

    def test_ipa_configuration_manager_is_packaged(self) -> None:
        text = DEVICE_MK.read_text(encoding="utf-8")
        for package in ("ipacm", "IPACM_cfg.xml"):
            self.assertRegex(text, rf"(?m)^\s*{re.escape(package)}(?:\s*\\)?$")


if __name__ == "__main__":
    unittest.main()
