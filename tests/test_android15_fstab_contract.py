from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FSTAB = ROOT / "rootdir" / "etc" / "fstab.qcom"
RECOVERY = ROOT / "rootdir" / "etc" / "recovery.fstab"
UFS = "/dev/block/platform/soc/1da4000.ufshc/by-name/"


def entries(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 5:
            out[fields[1]] = fields
    return out


class Android15FstabContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = FSTAB.read_text(encoding="utf-8")
        self.recovery_text = RECOVERY.read_text(encoding="utf-8")
        self.rows = entries(self.text)

    def test_recovery_and_vendor_fstab_share_one_mount_contract(self) -> None:
        self.assertEqual(self.recovery_text, self.text)

    def test_system_and_vendor_are_ab_first_stage_mounts(self) -> None:
        for mount in ("/system", "/vendor"):
            row = self.rows[mount]
            self.assertTrue(row[0].startswith(UFS), row)
            flags = set(row[4].split(","))
            self.assertTrue({"wait", "slotselect", "first_stage_mount"} <= flags, row)

    def test_userdata_is_android15_fbe_not_stock_fde(self) -> None:
        row = self.rows["/data"]
        self.assertEqual(row[0], UFS + "userdata")
        flags = set(row[4].split(","))
        self.assertTrue({"wait", "check", "latemount", "formattable", "fileencryption=ice", "quota"} <= flags, row)
        self.assertNotIn("encryptable=footer", row[4])
        self.assertNotIn("forceencrypt", row[4])

    def test_firmware_and_persist_mounts_use_real_red_ufs_paths(self) -> None:
        expected = {
            "/vendor/firmware_mnt": "modem",
            "/vendor/bt_firmware": "bluetooth",
            "/vendor/dsp": "dsp",
            "/mnt/vendor/persist": "persist",
        }
        for mount, part in expected.items():
            self.assertEqual(self.rows[mount][0], UFS + part)

    def test_zram_and_removable_storage_contract_remain_present(self) -> None:
        self.assertIn("/dev/block/zram0", self.text)
        self.assertIn("voldmanaged=sdcard1:auto", self.text)
        self.assertIn("voldmanaged=usb:auto", self.text)


if __name__ == "__main__":
    unittest.main()
