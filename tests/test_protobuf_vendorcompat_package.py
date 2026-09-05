from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ProtobufVendorcompatPackageTest(unittest.TestCase):
    def test_lineage_vendorcompat_provider_is_packaged(self):
        text = (ROOT / "device.mk").read_text(encoding="utf-8")
        self.assertIn("libprotobuf-cpp-full-vendorcompat", text)
        self.assertNotIn("vendor/lib/libprotobuf-cpp-full.so", text)
        self.assertNotIn("vendor/lib64/libprotobuf-cpp-full.so", text)
