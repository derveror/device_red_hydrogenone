from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.analysis.source_lock import (
    main,
    reference_records_from_inventory,
    validate_source_lock,
)


class SourceLockTest(unittest.TestCase):
    def test_reports_exact_field_mismatch(self) -> None:
        lock = {
            "reference_archives": [
                {
                    "archive": "tree.zip",
                    "sha256": "expected",
                    "archive_size_bytes": 10,
                    "uncompressed_size_bytes": 20,
                    "file_count": 1,
                    "root_directory": "tree",
                    "embedded_source_commit": "abc",
                }
            ]
        }
        inventory = [
            {
                "archive": "tree.zip",
                "archive_sha256": "actual",
                "archive_size_bytes": 10,
                "uncompressed_size_bytes": 20,
                "file_count": 1,
                "root_directory": "tree",
                "embedded_source_commit": "abc",
            }
        ]

        self.assertEqual(
            validate_source_lock(lock, inventory),
            ["tree.zip: sha256 expected expected, got actual"],
        )

    def test_reports_missing_unexpected_and_duplicate_archives(self) -> None:
        lock = {
            "reference_archives": [
                {"archive": "locked.zip"},
                {"archive": "locked.zip"},
                {"archive": "missing.zip"},
            ]
        }
        inventory = [
            {"archive": "locked.zip"},
            {"archive": "unexpected.zip"},
            {"archive": "unexpected.zip"},
        ]

        errors = validate_source_lock(lock, inventory)

        self.assertIn("source lock: duplicate archive: locked.zip", errors)
        self.assertIn("inventory: duplicate archive: unexpected.zip", errors)
        self.assertIn("missing archive from inventory: missing.zip", errors)
        self.assertIn("unexpected archive in inventory: unexpected.zip", errors)

    def test_reference_records_are_sorted_and_map_inventory_fields(self) -> None:
        inventory = [
            {
                "archive": "z.zip",
                "archive_sha256": "z-hash",
                "archive_size_bytes": 7,
                "uncompressed_size_bytes": 8,
                "file_count": 2,
                "root_directory": "z-root",
                "embedded_source_commit": "z-commit",
            },
            {
                "archive": "a.zip",
                "archive_sha256": "a-hash",
                "archive_size_bytes": 3,
                "uncompressed_size_bytes": 4,
                "file_count": 1,
                "root_directory": "a-root",
                "embedded_source_commit": None,
            },
        ]

        records = reference_records_from_inventory(inventory)

        self.assertEqual([record["archive"] for record in records], ["a.zip", "z.zip"])
        self.assertEqual(records[0]["sha256"], "a-hash")
        self.assertEqual(records[1]["embedded_source_commit"], "z-commit")

    def test_validate_cli_returns_zero_and_reports_count(self) -> None:
        inventory = [
            {
                "archive": "tree.zip",
                "archive_sha256": "hash",
                "archive_size_bytes": 10,
                "uncompressed_size_bytes": 20,
                "file_count": 1,
                "root_directory": "tree",
                "embedded_source_commit": "abc",
            }
        ]
        lock = {"reference_archives": reference_records_from_inventory(inventory)}

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lock_path = root / "lock.json"
            inventory_path = root / "inventory.json"
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                status = main(
                    [
                        "--validate",
                        "--lock",
                        str(lock_path),
                        "--inventory",
                        str(inventory_path),
                    ]
                )

        self.assertEqual(status, 0)
        self.assertEqual(stdout.getvalue(), "source lock verified: 1 archives\n")

    def test_write_cli_preserves_non_reference_sections(self) -> None:
        inventory = [
            {
                "archive": "tree.zip",
                "archive_sha256": "hash",
                "archive_size_bytes": 10,
                "uncompressed_size_bytes": 20,
                "file_count": 1,
                "root_directory": "tree",
                "embedded_source_commit": "abc",
            }
        ]
        lock = {"schema_version": 1, "project": "keep", "reference_archives": []}

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lock_path = root / "lock.json"
            inventory_path = root / "inventory.json"
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                status = main(
                    [
                        "--write-reference-section",
                        "--lock",
                        str(lock_path),
                        "--inventory",
                        str(inventory_path),
                    ]
                )
            result = json.loads(lock_path.read_text(encoding="utf-8"))

        self.assertEqual(status, 0)
        self.assertEqual(result["project"], "keep")
        self.assertEqual(result["reference_archives"][0]["archive"], "tree.zip")


if __name__ == "__main__":
    unittest.main()
