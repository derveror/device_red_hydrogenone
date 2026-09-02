from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "analysis" / "device_stock_config_audit.py"


class DeviceStockConfigAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("device_stock_config_audit", TOOL)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {TOOL}")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def make_roots(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        td = tempfile.TemporaryDirectory()
        base = Path(td.name)
        device = base / "device"
        stock = base / "stock-vendor"
        device.mkdir()
        stock.mkdir()
        return td, device, stock

    def test_identical_local_vendor_copy_is_reported(self) -> None:
        td, device, stock = self.make_roots()
        self.addCleanup(td.cleanup)
        (device / "configs").mkdir()
        (stock / "etc").mkdir()
        (device / "configs/a.conf").write_text("same\n", encoding="utf-8")
        (stock / "etc/a.conf").write_text("same\n", encoding="utf-8")
        (device / "device.mk").write_text(
            "PRODUCT_COPY_FILES += \\\n    $(LOCAL_PATH)/configs/a.conf:$(TARGET_COPY_OUT_VENDOR)/etc/a.conf\n",
            encoding="utf-8",
        )
        report = self.module.build_report(device, stock)
        self.assertEqual(report["summary"], {"different": 0, "identical": 1, "missing_device_source": 0, "missing_in_stock": 0, "total": 1})
        self.assertEqual(report["rows"][0]["status"], "identical")
        self.assertEqual(report["rows"][0]["destination"], "vendor/etc/a.conf")

    def test_different_and_missing_stock_are_distinguished(self) -> None:
        td, device, stock = self.make_roots()
        self.addCleanup(td.cleanup)
        (device / "configs").mkdir()
        (stock / "etc").mkdir()
        (device / "configs/a.conf").write_text("device\n", encoding="utf-8")
        (device / "configs/b.conf").write_text("device-only\n", encoding="utf-8")
        (stock / "etc/a.conf").write_text("stock\n", encoding="utf-8")
        (device / "device.mk").write_text(
            "PRODUCT_COPY_FILES += \\\n"
            "    $(LOCAL_PATH)/configs/a.conf:$(TARGET_COPY_OUT_VENDOR)/etc/a.conf \\\n"
            "    $(LOCAL_PATH)/configs/b.conf:$(TARGET_COPY_OUT_VENDOR)/etc/b.conf\n",
            encoding="utf-8",
        )
        report = self.module.build_report(device, stock)
        by_dest = {row["destination"]: row for row in report["rows"]}
        self.assertEqual(by_dest["vendor/etc/a.conf"]["status"], "different")
        self.assertEqual(by_dest["vendor/etc/b.conf"]["status"], "missing_in_stock")
        self.assertNotEqual(by_dest["vendor/etc/a.conf"]["device_sha256"], by_dest["vendor/etc/a.conf"]["stock_sha256"])

    def test_foreach_wildcard_local_copy_is_expanded(self) -> None:
        td, device, stock = self.make_roots()
        self.addCleanup(td.cleanup)
        init = device / "rootdir/etc/init/hw"
        init.mkdir(parents=True)
        stock_init = stock / "etc/init/hw"
        stock_init.mkdir(parents=True)
        (init / "init.alpha.rc").write_text("on boot\n", encoding="utf-8")
        (stock_init / "init.alpha.rc").write_text("on boot\n", encoding="utf-8")
        (device / "device.mk").write_text(
            "$(foreach f,$(wildcard $(LOCAL_PATH)/rootdir/etc/init/hw/*.rc),\\\n"
            "    $(eval PRODUCT_COPY_FILES += $(f):$(TARGET_COPY_OUT_VENDOR)/etc/init/hw/$(notdir $(f))))\n",
            encoding="utf-8",
        )
        report = self.module.build_report(device, stock)
        self.assertEqual(report["rows"][0]["source"], "rootdir/etc/init/hw/init.alpha.rc")
        self.assertEqual(report["rows"][0]["destination"], "vendor/etc/init/hw/init.alpha.rc")
        self.assertEqual(report["rows"][0]["status"], "identical")

    def test_missing_local_source_is_a_hard_audit_row(self) -> None:
        td, device, stock = self.make_roots()
        self.addCleanup(td.cleanup)
        (device / "device.mk").write_text(
            "PRODUCT_COPY_FILES += \\\n    $(LOCAL_PATH)/configs/missing.conf:$(TARGET_COPY_OUT_VENDOR)/etc/missing.conf\n",
            encoding="utf-8",
        )
        report = self.module.build_report(device, stock)
        self.assertEqual(report["rows"][0]["status"], "missing_device_source")
        self.assertEqual(report["summary"]["missing_device_source"], 1)


if __name__ == "__main__":
    unittest.main()
