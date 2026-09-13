from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVICE_MK = ROOT / "device.mk"


def product_packages(text: str) -> set[str]:
    package_text = "\n".join(
        block.group(1)
        for block in re.finditer(
            r"PRODUCT_PACKAGES\s*\+=\s*\\\n(.*?)(?=\n\n|\n[A-Z_]+\s*[:+?]?=|\Z)",
            text,
            re.S,
        )
    )
    return set(
        re.findall(r"(?m)^\s*([A-Za-z0-9_.@+:-]+)\s*\\?\s*$", package_text)
    )


class Red118KeymasterSelectionTest(unittest.TestCase):
    def test_device_does_not_select_the_generic_file_firmware_keymaster(self) -> None:
        packages = product_packages(DEVICE_MK.read_text(encoding="utf-8"))
        self.assertNotIn("android.hardware.keymaster@3.0-impl", packages)
        self.assertNotIn("android.hardware.keymaster@3.0-service", packages)

    def test_device_records_vendor_ownership_of_red118_keymaster(self) -> None:
        text = DEVICE_MK.read_text(encoding="utf-8")
        self.assertIn("RED .118 QTI Keymaster", text)
        self.assertIn("vendor/red/hydrogenone/hydrogenone-vendor.mk", text)


if __name__ == "__main__":
    unittest.main()
