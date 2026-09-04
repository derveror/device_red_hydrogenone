from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GnssCherylAbiContractTest(unittest.TestCase):
    def test_product_uses_legacy_qualcomm_gnss_hidl_1_0_frontend(self) -> None:
        device = (ROOT / "device.mk").read_text(encoding="utf-8")
        self.assertIn("android.hardware.gnss@1.0-impl-qti", device)
        self.assertIn("android.hardware.gnss@1.0-service-qti", device)
        self.assertNotIn("android.hardware.gnss@2.1-impl-qti", device)
        self.assertNotIn("android.hardware.gnss@2.1-service-qti", device)
        self.assertNotIn("libbatching", device)
        self.assertNotIn("libgeofencing", device)

    def test_device_manifest_owns_gnss_1_0_default_instance(self) -> None:
        root = ET.parse(ROOT / "manifest.xml").getroot()
        found = []
        for hal in root.findall("hal"):
            if hal.findtext("name") != "android.hardware.gnss":
                continue
            version = hal.findtext("version")
            for interface in hal.findall("interface"):
                if interface.findtext("name") != "IGnss":
                    continue
                for instance in interface.findall("instance"):
                    if instance.text:
                        found.append((version, instance.text.strip()))
        self.assertEqual(found, [("1.0", "default")])

    def test_legacy_loc_api_base_abi_required_by_red118_is_present(self) -> None:
        text = (ROOT / "gps/core/LocApiBase.h").read_text(encoding="utf-8")
        required = (
            r"LocApiBase\s*\(\s*const MsgTask\*\s+msgTask",
            r"enableData\s*\(\s*int\s+enable\s*\)",
            r"setAPN\s*\(\s*char\*\s+apn\s*,\s*int\s+len\s*\)",
            r"requestATL\s*\(\s*int\s+connHandle\s*,\s*LocAGpsType\s+agps_type\s*\)",
            r"requestSuplES\s*\(\s*int\s+connHandle\s*\)",
            r"reportDataCallOpened\s*\(\s*\)",
            r"reportDataCallClosed\s*\(\s*\)",
            r"saveSupportedMsgList\s*\(\s*uint64_t\s+supportedMsgList\s*\)",
            r"saveSupportedFeatureList\s*\(\s*uint8_t\s*\*\s*featureList\s*\)",
        )
        for pattern in required:
            self.assertRegex(text, pattern)

    def test_legacy_gps_utils_symbols_required_by_red118_are_declared(self) -> None:
        cfg = (ROOT / "gps/utils/loc_cfg.h").read_text(encoding="utf-8")
        msg = (ROOT / "gps/utils/MsgTask.h").read_text(encoding="utf-8")
        log = (ROOT / "gps/utils/loc_log.h").read_text(encoding="utf-8")
        self.assertRegex(cfg, r"\bloc_read_conf\s*\(")
        self.assertRegex(log, r"\bloc_get_name_from_val\s*\(")
        self.assertRegex(msg, r"sendMsg\s*\(\s*const LocMsg\*\s+msg\s*\)\s+const")
        self.assertRegex(cfg, r"\bloc_modem_emulator_enabled\s*\(")

    def test_only_one_active_qti_gnss_frontend_generation_exists(self) -> None:
        self.assertTrue((ROOT / "gps/android/Android.bp").is_file())
        self.assertFalse((ROOT / "gps/android/2.1/Android.bp").exists())
        android_bp = (ROOT / "gps/android/Android.bp").read_text(encoding="utf-8")
        self.assertIn('name: "android.hardware.gnss@1.0-impl-qti"', android_bp)
        self.assertIn('name: "android.hardware.gnss@1.0-service-qti"', android_bp)


if __name__ == "__main__":
    unittest.main()
