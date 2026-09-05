from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "apply_reference_ril_header_fix.py"

SAMPLE = """cc_library_shared {
    name: "libreference-ril",
    srcs: [
        "reference-ril.c",
    ],
    shared_libs: [
        "libril",
    ],
    static_libs: ["libbase"],
    cflags: [
        "-Werror",
    ],
    vendor: true,
}
"""


class ReferenceRilHeaderFixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("ril_fix", TOOL)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load platform patch tool")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_adds_ril_headers_to_reference_ril(self) -> None:
        patched, changed = self.module.patch_android_bp(SAMPLE)
        self.assertTrue(changed)
        self.assertIn('header_libs: ["ril_headers"],', patched)
        self.assertLess(
            patched.index('header_libs: ["ril_headers"],'),
            patched.index("cflags:"),
        )

    def test_patch_is_idempotent(self) -> None:
        once, changed_once = self.module.patch_android_bp(SAMPLE)
        twice, changed_twice = self.module.patch_android_bp(once)
        self.assertTrue(changed_once)
        self.assertFalse(changed_twice)
        self.assertEqual(once, twice)
        self.assertEqual(once.count('header_libs: ["ril_headers"],'), 1)

    def test_rejects_unexpected_upstream_layout(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected libreference-ril"):
            self.module.patch_android_bp('cc_library_shared { name: "other"; }\n')

    def test_cli_patches_requested_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "Android.bp"
            path.write_text(SAMPLE, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(TOOL), "--file", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PATCHED", result.stdout)
            self.assertIn(
                'header_libs: ["ril_headers"],',
                path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
