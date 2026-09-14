from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVICE_MK = ROOT / "device.mk"
VENDOR_PROP = ROOT / "vendor.prop"
USB_INIT = ROOT / "rootdir/etc/init/hw/init.qcom.usb.rc"
BOARD_CONFIG = ROOT / "BoardConfig.mk"
VENDOR_FILE_CONTEXTS = ROOT / "sepolicy/vendor/file_contexts"


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


def properties(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value
    return result


class Android15UsbGadgetContractTest(unittest.TestCase):
    def test_product_installs_controller_agnostic_qti_gadget_hal(self) -> None:
        packages = product_packages(DEVICE_MK.read_text(encoding="utf-8"))
        self.assertIn("android.hardware.usb.gadget-service.qti", packages)
        self.assertIn("usb_compositions.conf", packages)
        self.assertNotIn("android.hardware.usb.gadget@1.1-service", packages)
        self.assertNotIn("android.hardware.usb.gadget@1.2-service", packages)

    def test_gadget_hal_uses_the_red118_usb_controller(self) -> None:
        props = properties(VENDOR_PROP.read_text(encoding="utf-8"))
        self.assertEqual(props.get("vendor.usb.controller"), "a800000.dwc3")
        self.assertEqual(props.get("vendor.usb.use_gadget_hal"), "1")
        self.assertEqual(props.get("vendor.usb.use_ffs_mtp"), "1")
        self.assertEqual(props.get("vendor.usb.rndis.func.name"), "rndis")

    def test_qti_gadget_service_uses_the_shared_qcom_usb_domain(self) -> None:
        board_config = BOARD_CONFIG.read_text(encoding="utf-8")
        contexts = VENDOR_FILE_CONTEXTS.read_text(encoding="utf-8")
        self.assertIn(
            "include device/qcom/sepolicy-legacy-um/SEPolicy.mk", board_config
        )
        self.assertNotRegex(
            contexts,
            r"android\\\.hardware\\\.usb\\\.gadget-service\\\.qti",
        )

    def test_init_provides_the_configfs_and_functionfs_foundation(self) -> None:
        init = USB_INIT.read_text(encoding="utf-8")
        required_commands = (
            "mount configfs none /config",
            "mkdir /config/usb_gadget/g1 0770 system usb",
            "mkdir /config/usb_gadget/g1/strings/0x409 0770 system usb",
            "mkdir /config/usb_gadget/g1/configs/b.1 0770 system usb",
            "mkdir /config/usb_gadget/g1/configs/b.1/strings/0x409 0770 system usb",
            "mkdir /config/usb_gadget/g1/functions/ffs.adb 0770 system usb",
            "mkdir /config/usb_gadget/g1/functions/ffs.mtp 0770 system usb",
            "mkdir /config/usb_gadget/g1/functions/ffs.ptp 0770 system usb",
            "mkdir /config/usb_gadget/g1/functions/rndis.rndis 0770 system usb",
            "mkdir /dev/usb-ffs/adb 0770 shell system",
            "mkdir /dev/usb-ffs/mtp 0770 mtp mtp",
            "mkdir /dev/usb-ffs/ptp 0770 mtp mtp",
            "mount functionfs adb /dev/usb-ffs/adb uid=2000,gid=1000,rmode=0770,fmode=0660",
            "mount functionfs mtp /dev/usb-ffs/mtp rmode=0770,fmode=0660,uid=1024,gid=1024,no_disconnect=1",
            "mount functionfs ptp /dev/usb-ffs/ptp rmode=0770,fmode=0660,uid=1024,gid=1024,no_disconnect=1",
            "symlink /config/usb_gadget/g1/configs/b.1 /config/usb_gadget/g1/os_desc/b.1",
            "chown system usb /config/usb_gadget/g1/UDC",
            "chown system usb /config/usb_gadget/g1/idProduct",
            "chown system usb /config/usb_gadget/g1/idVendor",
            "setprop vendor.usb.controller ${sys.usb.controller}",
            "setprop sys.usb.controller a800000.dwc3",
            "setprop sys.usb.configfs 2",
            "setprop vendor.usb.config ${sys.usb.config}",
        )
        for command in required_commands:
            with self.subTest(command=command):
                self.assertIn(command, init)


if __name__ == "__main__":
    unittest.main()
