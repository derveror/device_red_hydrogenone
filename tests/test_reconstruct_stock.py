from __future__ import annotations

import contextlib
import hashlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.analysis.reconstruct_stock import main, reconstruct


class ReconstructStockTest(unittest.TestCase):
    def test_reconstructs_manifest_order_and_verifies_final_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "stock.00.part").write_bytes(b"abc")
            (root / "stock.01.part").write_bytes(b"def")
            manifest = root / "parts.sha256"
            manifest.write_text(
                f"{hashlib.sha256(b'abc').hexdigest()}  stock.00.part\n"
                f"{hashlib.sha256(b'def').hexdigest()}  stock.01.part\n",
                encoding="utf-8",
            )
            output = root / "stock.rar"

            reconstruct(
                root,
                manifest,
                output,
                hashlib.sha256(b"abcdef").hexdigest(),
            )

            self.assertEqual(output.read_bytes(), b"abcdef")
            self.assertFalse((root / "stock.rar.partial").exists())

    def test_corrupt_part_is_rejected_before_partial_output_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            part = root / "stock.00.part"
            part.write_bytes(b"corrupt")
            manifest = root / "parts.sha256"
            manifest.write_text(
                f"{hashlib.sha256(b'expected').hexdigest()}  {part.name}\n",
                encoding="utf-8",
            )
            output = root / "stock.rar"

            with self.assertRaisesRegex(ValueError, "stock[.]00[.]part"):
                reconstruct(root, manifest, output, hashlib.sha256(b"expected").hexdigest())

            self.assertFalse(output.exists())
            self.assertFalse((root / "stock.rar.partial").exists())

    def test_wrong_final_hash_leaves_no_output_or_partial_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            part = root / "stock.00.part"
            part.write_bytes(b"abc")
            manifest = root / "parts.sha256"
            manifest.write_text(
                f"{hashlib.sha256(b'abc').hexdigest()}  {part.name}\n",
                encoding="utf-8",
            )
            output = root / "stock.rar"

            with self.assertRaisesRegex(ValueError, "final archive"):
                reconstruct(root, manifest, output, hashlib.sha256(b"wrong").hexdigest())

            self.assertFalse(output.exists())
            self.assertFalse((root / "stock.rar.partial").exists())

    def test_manifest_order_controls_concatenation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "stock.00.part").write_bytes(b"first")
            (root / "stock.01.part").write_bytes(b"second")
            manifest = root / "parts.sha256"
            manifest.write_text(
                f"{hashlib.sha256(b'second').hexdigest()}  stock.01.part\n"
                f"{hashlib.sha256(b'first').hexdigest()}  stock.00.part\n",
                encoding="utf-8",
            )
            output = root / "stock.rar"
            expected = hashlib.sha256(b"secondfirst").hexdigest()

            reconstruct(root, manifest, output, expected)

            self.assertEqual(output.read_bytes(), b"secondfirst")

    def test_path_traversal_filename_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "parts.sha256"
            manifest.write_text(
                f"{'0' * 64}  ../outside.part\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "unsafe part filename"):
                reconstruct(root, manifest, root / "stock.rar", "0" * 64)

    def test_duplicate_part_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            digest = hashlib.sha256(b"abc").hexdigest()
            (root / "stock.part").write_bytes(b"abc")
            manifest = root / "parts.sha256"
            manifest.write_text(
                f"{digest}  stock.part\n{digest}  stock.part\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate part: stock[.]part"):
                reconstruct(root, manifest, root / "stock.rar", digest)

    def test_malformed_manifest_hash_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "parts.sha256"
            manifest.write_text("not-a-hash  stock.part\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid SHA-256"):
                reconstruct(root, manifest, root / "stock.rar", "0" * 64)

    def test_missing_part_is_reported_before_output_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "parts.sha256"
            manifest.write_text(f"{'0' * 64}  missing.part\n", encoding="utf-8")
            output = root / "stock.rar"

            with self.assertRaisesRegex(ValueError, "missing part: missing[.]part"):
                reconstruct(root, manifest, output, "0" * 64)

            self.assertFalse(output.exists())

    def test_existing_output_is_preserved_without_explicit_replace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            part = root / "stock.part"
            part.write_bytes(b"new")
            digest = hashlib.sha256(b"new").hexdigest()
            manifest = root / "parts.sha256"
            manifest.write_text(f"{digest}  stock.part\n", encoding="utf-8")
            output = root / "stock.rar"
            output.write_bytes(b"keep")

            with self.assertRaises(FileExistsError):
                reconstruct(root, manifest, output, digest)

            self.assertEqual(output.read_bytes(), b"keep")

    def test_replace_true_atomically_replaces_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            part = root / "stock.part"
            part.write_bytes(b"new")
            digest = hashlib.sha256(b"new").hexdigest()
            manifest = root / "parts.sha256"
            manifest.write_text(f"{digest}  stock.part\n", encoding="utf-8")
            output = root / "stock.rar"
            output.write_bytes(b"old")

            reconstruct(root, manifest, output, digest, replace=True)

            self.assertEqual(output.read_bytes(), b"new")

    def test_cli_reports_verified_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            part = root / "stock.part"
            part.write_bytes(b"payload")
            digest = hashlib.sha256(b"payload").hexdigest()
            manifest = root / "parts.sha256"
            manifest.write_text(f"{digest}  stock.part\n", encoding="utf-8")
            output = root / "stock.rar"
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                status = main(
                    [
                        "--parts-dir",
                        str(root),
                        "--manifest",
                        str(manifest),
                        "--output",
                        str(output),
                        "--expected-sha256",
                        digest,
                    ]
                )

            self.assertEqual(status, 0)
            self.assertEqual(output.read_bytes(), b"payload")
            self.assertIn("reconstructed and verified", stdout.getvalue())

    def test_cli_returns_one_for_hash_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            part = root / "stock.part"
            part.write_bytes(b"payload")
            manifest = root / "parts.sha256"
            manifest.write_text(f"{'0' * 64}  stock.part\n", encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                status = main(
                    [
                        "--parts-dir",
                        str(root),
                        "--manifest",
                        str(manifest),
                        "--output",
                        str(root / "stock.rar"),
                        "--expected-sha256",
                        "0" * 64,
                    ]
                )

            self.assertEqual(status, 1)
            self.assertIn("stock.part", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
