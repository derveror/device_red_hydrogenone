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


class RadioRuntimeRestoreContractTest(unittest.TestCase):
    def test_bluetooth_vendor_library_is_packaged(self) -> None:
        packages = make_variable_tokens(
            (ROOT / "device.mk").read_text(encoding="utf-8"), "PRODUCT_PACKAGES"
        )
        self.assertIn("libbt-vendor", packages)

    def test_exact_stock118_cherokee_property_exists(self) -> None:
        properties = {
            line.strip()
            for line in (ROOT / "vendor.prop").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertIn("vendor.qcom.bluetooth.soc=cherokee", properties)

    def test_stock118_wlan_mac_symlink_is_declared_and_packaged(self) -> None:
        bp = (ROOT / "Android.bp").read_text(encoding="utf-8")
        self.assertRegex(
            bp,
            r'(?s)install_symlink\s*\{.*?name:\s*"wlan_mac_bin_symlink".*?'
            r'vendor:\s*true.*?installed_location:\s*'
            r'"firmware/wlan/qca_cld/wlan_mac.bin".*?symlink_target:\s*'
            r'"/mnt/vendor/persist/wlan_mac.bin".*?\}',
        )
        packages = make_variable_tokens(
            (ROOT / "device.mk").read_text(encoding="utf-8"), "PRODUCT_PACKAGES"
        )
        self.assertIn("wlan_mac_bin_symlink", packages)


if __name__ == "__main__":
    unittest.main()
