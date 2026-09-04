from __future__ import annotations

import unittest
from pathlib import Path

from tools.hidlbase_shim_fixup_paths import (
    EXPECTED_HIDLBASE_SHIM_FIXUP_COUNT,
    HIDLBASE_SHIM_FIXUP_PATHS,
)

ROOT = Path(__file__).resolve().parents[1]


class LegacyHidlShimFixupContractTest(unittest.TestCase):
    def test_exact_red118_fixup_set_is_locked(self) -> None:
        paths = set(HIDLBASE_SHIM_FIXUP_PATHS)
        self.assertEqual(len(paths), EXPECTED_HIDLBASE_SHIM_FIXUP_COUNT)
        self.assertEqual(EXPECTED_HIDLBASE_SHIM_FIXUP_COUNT, 63)
        self.assertTrue(all(path.startswith(('vendor/lib/', 'vendor/lib64/')) for path in paths))
        self.assertTrue(all(path.endswith('.so') for path in paths))

    def test_extraction_reapplies_lineage_hidlbase_shim(self) -> None:
        text = (ROOT / 'extract-files.py').read_text(encoding='utf-8')
        self.assertIn('HIDLBASE_SHIM_FIXUP_PATHS', text)
        self.assertIn("blob_fixup().add_needed('libhidlbase_shim.so')", text)


if __name__ == '__main__':
    unittest.main()
