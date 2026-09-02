from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "BoardConfig.mk"
PRODUCT = ROOT / "lineage_hydrogenone.mk"


class VendorInheritanceContractTest(unittest.TestCase):
    def test_boardconfig_requires_generated_vendor_boardconfig(self) -> None:
        text = BOARD.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"(?m)^\s*include\s+vendor/red/hydrogenone/BoardConfigVendor\.mk\s*$",
        )
        self.assertNotRegex(
            text,
            r"(?m)^\s*-include\s+vendor/red/hydrogenone/BoardConfigVendor\.mk\s*$",
        )

    def test_product_requires_generated_vendor_makefile(self) -> None:
        text = PRODUCT.read_text(encoding="utf-8")
        self.assertIn(
            "$(call inherit-product, vendor/red/hydrogenone/hydrogenone-vendor.mk)",
            text,
        )
        self.assertNotIn(
            "inherit-product-if-exists, vendor/red/hydrogenone/hydrogenone-vendor.mk",
            text,
        )

    def test_vendor_is_inherited_before_device_definition(self) -> None:
        text = PRODUCT.read_text(encoding="utf-8")
        vendor_pos = text.find("vendor/red/hydrogenone/hydrogenone-vendor.mk")
        device_pos = text.find("device/red/hydrogenone/device.mk")
        self.assertGreaterEqual(vendor_pos, 0)
        self.assertGreaterEqual(device_pos, 0)
        self.assertLess(vendor_pos, device_pos)


if __name__ == "__main__":
    unittest.main()
