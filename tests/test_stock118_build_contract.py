from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "BoardConfig.mk"
PRODUCT = ROOT / "lineage_hydrogenone.mk"
PREBUILT = ROOT / "prebuilt" / "Image.gz-dtb"
BOOT_CONTRACT = ROOT / "docs" / "stock" / "h1a1000-r118" / "boot-image-contract.json"
STOCK_META = ROOT / "docs" / "stock" / "h1a1000-r118" / "inventory-summary.json"


def make_value(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*:?=\s*([^#\n]+)", text)
    return match.group(1).strip() if match else None


class Stock118BuildContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.board = BOARD.read_text(encoding="utf-8")
        cls.product = PRODUCT.read_text(encoding="utf-8")
        cls.boot = json.loads(BOOT_CONTRACT.read_text(encoding="utf-8"))
        cls.stock = json.loads(STOCK_META.read_text(encoding="utf-8"))

    def test_boot_header_and_load_addresses_match_canonical_118(self) -> None:
        header = self.boot["header"]
        self.assertEqual(make_value(self.board, "BOARD_BOOT_HEADER_VERSION"), str(header["header_version"]))
        self.assertEqual(make_value(self.board, "BOARD_KERNEL_PAGESIZE"), str(header["page_size"]))
        self.assertEqual(make_value(self.board, "BOARD_KERNEL_OFFSET"), header["kernel_addr"])
        self.assertEqual(make_value(self.board, "BOARD_RAMDISK_OFFSET"), header["ramdisk_addr"])
        self.assertEqual(make_value(self.board, "BOARD_SECOND_OFFSET"), header["second_addr"])
        self.assertEqual(make_value(self.board, "BOARD_TAGS_OFFSET"), header["tags_addr"])

    def test_partition_sizes_match_canonical_118_partition_xml(self) -> None:
        expected = {}
        for row in self.boot["partition_xml_records"]:
            attrs = row.get("attributes", {})
            label = attrs.get("label", "")
            if label in {"boot_a", "system_a", "vendor_a"}:
                expected[label] = int(attrs["size_in_kb"]) * 1024
        self.assertEqual(make_value(self.board, "BOARD_BOOTIMAGE_PARTITION_SIZE"), str(expected["boot_a"]))
        self.assertEqual(make_value(self.board, "BOARD_SYSTEMIMAGE_PARTITION_SIZE"), str(expected["system_a"]))
        self.assertEqual(make_value(self.board, "BOARD_VENDORIMAGE_PARTITION_SIZE"), str(expected["vendor_a"]))

    def test_vendor_security_patch_matches_canonical_118(self) -> None:
        expected = self.stock["build"]["vendor_security_patch"]
        self.assertEqual(make_value(self.board, "VENDOR_SECURITY_PATCH"), expected)

    def test_product_identity_uses_canonical_118_fingerprint(self) -> None:
        expected = self.boot["build_properties"]["ro.build.fingerprint"]
        self.assertIn(f"BuildFingerprint={expected}", self.product)
        self.assertNotIn("H1A1000.010ho.01.01.01r.109", self.product)
        self.assertNotIn(":8.1.0/", self.product)

    def test_forced_prebuilt_kernel_is_exact_canonical_118_kernel(self) -> None:
        self.assertEqual(make_value(self.board, "TARGET_FORCE_PREBUILT_KERNEL"), "true")
        self.assertEqual(make_value(self.board, "TARGET_PREBUILT_KERNEL"), "$(DEVICE_PATH)/prebuilt/Image.gz-dtb")
        data = PREBUILT.read_bytes()
        self.assertEqual(len(data), self.boot["kernel"]["size"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), self.boot["kernel"]["sha256"])

    def test_boardconfig_does_not_claim_109_for_118_authoritative_fields(self) -> None:
        active_lines = "\n".join(
            line for line in self.board.splitlines()
            if any(token in line for token in ("Kernel", "Partitions", "VENDOR_SECURITY_PATCH", "TARGET_PREBUILT_KERNEL"))
        )
        self.assertNotIn(".109", active_lines)

    def test_unsupported_android_9_vndk_snapshot_is_removed_after_vendor_config(self) -> None:
        vendor_include = "include vendor/red/hydrogenone/BoardConfigVendor.mk"
        removal = "PRODUCT_EXTRA_VNDK_VERSIONS := $(filter-out 28,$(PRODUCT_EXTRA_VNDK_VERSIONS))"

        self.assertIn(vendor_include, self.board)
        self.assertIn(removal, self.board)
        self.assertGreater(self.board.index(removal), self.board.index(vendor_include))


if __name__ == "__main__":
    unittest.main()
