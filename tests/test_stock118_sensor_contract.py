from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANDROID_ROOT = ROOT.parents[2]
VENDOR_ROOT = ANDROID_ROOT / "vendor/red/hydrogenone"
DEVICE_PROPRIETARY_FILES = ROOT / "proprietary-files.txt"
VENDOR_PROPRIETARY_FILES = VENDOR_ROOT / "proprietary-files.txt"
VENDOR_PAYLOAD = VENDOR_ROOT / "proprietary"
QCOM_INIT = ROOT / "rootdir/etc/init/hw/init.qcom.rc"
DEVICE_MK = ROOT / "device.mk"

SENSOR_FILES = {
    "vendor/etc/sensors/hals.conf",
    "vendor/etc/sensors/sensor_def_qcomdev.conf",
    "vendor/lib/sensors.ssc.so",
    "vendor/lib64/sensors.ssc.so",
    "vendor/lib/libsensor_reg.so",
    "vendor/lib64/libsensor_reg.so",
    "vendor/lib/libsns_low_lat_stream_stub.so",
    "vendor/lib64/libsns_low_lat_stream_stub.so",
    "vendor/lib/libsdsprpc.so",
    "vendor/lib64/libsdsprpc.so",
}

STOCK118_SENSOR_IDENTITY = {
    "vendor/etc/sensors/hals.conf": (
        15,
        "79c1febf7ce0c06a9e2612a4137bbdaffb5ed6cd18c89415216e482a287a591b",
    ),
    "vendor/etc/sensors/sensor_def_qcomdev.conf": (
        235073,
        "4d7598e256ef1fc635e0fb0fe3b3f8744da971aedebcf07aa51c4eeb47d3e660",
    ),
    "vendor/lib/libsdsprpc.so": (
        117784,
        "3dc24df9741587dfae6ab055192eb2d7fafdcf3b615ce6399175a0b4e7bccd9f",
    ),
    "vendor/lib/libsensor_reg.so": (
        23956,
        "894a892a379ae3b8ff37106e8f043fad75faf2143f19f6ed474ba8274a442142",
    ),
    "vendor/lib/libsns_low_lat_stream_stub.so": (
        19728,
        "16237eb78b33a2ba639ddf65a3185d829fac648e37b5e9e6cd90c7a6de0a9dfe",
    ),
    "vendor/lib/sensors.ssc.so": (
        269580,
        "4577d967e891716170f07ff238f8c3df325d25194a7e4bfa3d349550cb0dbfa0",
    ),
    "vendor/lib64/libsdsprpc.so": (
        201904,
        "ff9b89a1b3ab288947be650539b592de126593defa8ac04e86e088c335ee039c",
    ),
    "vendor/lib64/libsensor_reg.so": (
        68336,
        "46b774e23ac9e7658e8eed1662cce4a53dd5f7cb64b19c589053dd65843df67a",
    ),
    "vendor/lib64/libsns_low_lat_stream_stub.so": (
        68208,
        "4703c95487b8331138b768b01f720e37ef735a84e58166068ca574a2a941a5fd",
    ),
    "vendor/lib64/sensors.ssc.so": (
        331288,
        "b37eb0b7034f5f170167d10a3009fa9f56a3962a98208028c2a1209621e50519",
    ),
}


def listed_paths(path: Path) -> set[str]:
    return {
        line.split("|", 1)[0].removeprefix("-").strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


class Stock118SensorContractTest(unittest.TestCase):
    def test_stock118_sensor_payload_is_owned_by_vendor(self) -> None:
        self.assertTrue(VENDOR_ROOT.is_dir(), "vendor/red/hydrogenone is required")
        self.assertTrue(SENSOR_FILES <= listed_paths(DEVICE_PROPRIETARY_FILES))
        self.assertTrue(SENSOR_FILES <= listed_paths(VENDOR_PROPRIETARY_FILES))
        missing = sorted(
            path for path in SENSOR_FILES if not (VENDOR_PAYLOAD / path).is_file()
        )
        self.assertEqual(missing, [])

    def test_sensor_payload_is_exact_stock118(self) -> None:
        self.assertEqual(set(STOCK118_SENSOR_IDENTITY), SENSOR_FILES)
        for path, (expected_size, expected_sha256) in STOCK118_SENSOR_IDENTITY.items():
            payload = (VENDOR_PAYLOAD / path).read_bytes()
            self.assertEqual(len(payload), expected_size, path)
            self.assertEqual(hashlib.sha256(payload).hexdigest(), expected_sha256, path)

    def test_multihal_loads_the_stock118_ssc_module(self) -> None:
        config = VENDOR_PAYLOAD / "vendor/etc/sensors/hals.conf"
        self.assertEqual(config.read_text(encoding="utf-8"), "sensors.ssc.so\n")

    def test_android15_wrapper_remains_source_owned(self) -> None:
        packages = DEVICE_MK.read_text(encoding="utf-8")
        self.assertRegex(
            packages,
            r"(?m)^\s*android\.hardware\.sensors@1\.0-service\s*\\?$",
        )
        self.assertRegex(
            packages,
            r"(?m)^\s*android\.hardware\.sensors@1\.0-impl:64\s*\\?$",
        )
        self.assertNotIn(
            "vendor/bin/hw/android.hardware.sensors@1.0-service",
            listed_paths(VENDOR_PROPRIETARY_FILES),
        )

    def test_qcom_init_starts_the_stock118_sensor_control_plane(self) -> None:
        text = QCOM_INIT.read_text(encoding="utf-8")
        self.assertIn("write /sys/kernel/boot_slpi/boot 1", text)
        self.assertIn("mkdir /mnt/vendor/persist/sensors 0770 system system", text)
        for stock_owned_path in (
            "/mnt/vendor/persist/sensors",
            "/mnt/vendor/persist/sensors/sns.reg",
            "/mnt/vendor/persist/sensors/sensors_list.txt",
            "/mnt/vendor/persist/sensors/registry",
            "/mnt/vendor/persist/sensors/registry/registry",
            "/mnt/vendor/persist/sensors/registry/registry/sensors_registry",
            "/mnt/vendor/persist/sensors/sensors_settings",
            "/mnt/vendor/persist/sensors/registry/sns_reg_config",
            "/mnt/vendor/persist/sensors/registry/sns_reg_version",
            "/mnt/vendor/persist/sensors/registry/config",
        ):
            self.assertIn(f"chown system system {stock_owned_path}", text)
        self.assertRegex(
            text,
            re.compile(
                r"service vendor\.sensors\.qti /vendor/bin/sensors\.qti\n"
                r"(?:\s+.*\n)*?\s+disabled",
                re.M,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"service vendor-sensor-sh /vendor/bin/init\.qcom\.sensors\.sh\n"
                r"(?:\s+.*\n)*?\s+oneshot",
                re.M,
            ),
        )


if __name__ == "__main__":
    unittest.main()
