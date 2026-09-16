from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def make_variable_tokens(text: str, variable: str) -> set[str]:
    values: set[str] = set()
    logical = ""
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        logical = f"{logical} {line}".strip()
        if logical.endswith("\\"):
            logical = logical[:-1].rstrip()
            continue
        match = re.match(rf"^{re.escape(variable)}\s*\+=\s*(.*)$", logical)
        if match:
            values.update(match.group(1).split())
        logical = ""
    return values


class RadioAndroid15CompatibilityTest(unittest.TestCase):
    def test_radio_config_frontend_and_backend_are_packaged(self) -> None:
        packages = make_variable_tokens(
            (ROOT / "device.mk").read_text(encoding="utf-8"), "PRODUCT_PACKAGES"
        )
        self.assertTrue(
            {
                "android.hardware.radio.c_shim@1.0",
                "android.hardware.radio.c_shim@1.1",
                "android.hardware.radio.c_shim@1.2",
                "android.hardware.radio.config@1.1-service.wrapper",
            }.issubset(packages)
        )

    def test_stock118_dsds_topology_is_exposed_to_framework(self) -> None:
        properties = {
            line.strip()
            for line in (ROOT / "vendor.prop").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertTrue(
            {
                "persist.radio.multisim.config=dsds",
                "persist.vendor.radio.apm_sim_not_pwdn=1",
                "persist.vendor.radio.custom_ecc=1",
                "persist.vendor.radio.rat_on=combine",
                "persist.vendor.radio.sib16_support=1",
            }.issubset(properties)
        )


if __name__ == "__main__":
    unittest.main()
