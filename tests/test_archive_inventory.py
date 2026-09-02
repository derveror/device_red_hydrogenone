from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from analysis_test_utils import write_zip
from tools.analysis.archive_inventory import inventory_zip


class ArchiveInventoryTest(unittest.TestCase):
    def test_strips_one_common_archive_root_and_sorts_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = write_zip(
                Path(directory) / "device.zip",
                {
                    "tree/BoardConfig.mk": b"board\n",
                    "tree/audio/policy.xml": b"audio\n",
                },
                comment="0123456789abcdef",
            )
            result = inventory_zip(archive)

        self.assertEqual(result["root_directory"], "tree")
        self.assertEqual(
            [item["path"] for item in result["files"]],
            ["BoardConfig.mk", "audio/policy.xml"],
        )
        self.assertEqual(result["embedded_source_commit"], "0123456789abcdef")

    def test_multiple_roots_do_not_get_stripped_and_directories_are_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = write_zip(
                Path(directory) / "mixed.zip",
                {
                    "alpha/": b"",
                    "alpha/file.txt": b"alpha",
                    "beta/file.txt": b"beta",
                },
            )
            result = inventory_zip(archive)

        self.assertIsNone(result["root_directory"])
        self.assertEqual(
            [item["path"] for item in result["files"]],
            ["alpha/file.txt", "beta/file.txt"],
        )

    def test_empty_file_is_retained(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = write_zip(
                Path(directory) / "empty.zip",
                {"tree/empty.conf": b""},
            )
            result = inventory_zip(archive)

        self.assertEqual(result["file_count"], 1)
        self.assertEqual(result["uncompressed_size_bytes"], 0)
        self.assertEqual(result["files"][0]["path"], "empty.conf")

    def test_single_root_level_file_is_not_mistaken_for_directory_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = write_zip(
                Path(directory) / "root-file.zip",
                {"README.md": b"read me"},
            )
            result = inventory_zip(archive)

        self.assertIsNone(result["root_directory"])
        self.assertEqual(result["files"][0]["path"], "README.md")

    def test_cli_output_is_byte_identical_across_repeated_runs(self) -> None:
        from tools.analysis.archive_inventory import main

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = write_zip(
                root / "stable.zip",
                {
                    "tree/z.txt": b"z",
                    "tree/a.txt": b"a",
                },
            )
            first = root / "first.json"
            second = root / "second.json"

            self.assertEqual(main(["--output", str(first), str(archive)]), 0)
            self.assertEqual(main(["--output", str(second), str(archive)]), 0)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertNotIn(b"\n  ", first.read_bytes())

    def test_cli_summary_only_omits_per_file_records(self) -> None:
        from tools.analysis.archive_inventory import main

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = write_zip(root / "summary.zip", {"tree/file": b"payload"})
            output = root / "summary.json"

            self.assertEqual(
                main(["--summary-only", "--output", str(output), str(archive)]),
                0,
            )
            import json

            payload = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(payload[0]["file_count"], 1)
        self.assertNotIn("files", payload[0])


if __name__ == "__main__":
    unittest.main()
