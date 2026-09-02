# Hydrogen One Reference Source Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic, tested tooling that inventories all supplied device/vendor ZIP archives, compares donor trees by normalized path and content, validates the checked-in source lock, and reconstructs the split RED `.118` stock archive safely when its parts arrive.

**Architecture:** Pure Python standard-library command-line tools live under `tools/analysis/`. They produce deterministic JSON and Markdown under `docs/reference/` and never infer device compatibility from matching names alone. Stock reconstruction is isolated from extraction: it verifies a part manifest and final SHA-256 before any RAR content is trusted.

**Tech Stack:** Python 3.10+, `unittest`, `zipfile`, `hashlib`, `json`, `pathlib`, GNU/Linux shell utilities only for invocation.

**Spec:** `docs/superpowers/specs/2026-09-02-hydrogenone-lineage22.2-design.md`

## Execution amendment: full reports and compact repository summaries

The connected GitHub write interface accepts UTF-8 text but cannot ingest local generated files by path. To preserve the complete analysis without embedding almost one megabyte of generated path arrays in connector calls, the implementation produces two deterministic forms:

- compact checked-in `archive-inventory.json` and `archive-comparisons.json` summaries containing archive hashes and exact counts;
- full per-file/path reports bundled as `hydrogenone-reference-analysis-2026-09-02.tar.xz` in the connected Google Drive, pinned by `docs/reference/full-artifacts.sha256`.

Both forms are generated from the same tools. `--summary-only` removes only per-file or per-path arrays; it does not change hashes or counts. The full bundle contains metadata and hashes, not proprietary file contents.

## Global Constraints

- Target LineageOS branch is exactly `lineage-22.2`, Android 15 / API 35.
- Never create `device/red/msm8998-common` or a RED MSM8998 common vendor repository.
- Adopted open donor configuration is flattened into `device/red/hydrogenone`; proprietary payload belongs to `vendor/red/hydrogenone`.
- The `.118` archive is authoritative only after part hashes, final SHA-256, RAR integrity, and extracted build properties are verified.
- All generated output must be deterministic: sorted paths, UTF-8, LF line endings, and stable JSON indentation.
- Never include unique per-device data or file contents from proprietary archives in generated reports; record only metadata and hashes.
- The current `main` branch remains unchanged; work occurs on `lineage-22.2-stock118-rework`.

## File Structure

- Create `tools/analysis/archive_inventory.py` — normalize ZIP roots and inventory archive/file metadata.
- Create `tools/analysis/tree_compare.py` — compare two normalized inventories by path and SHA-256.
- Create `tools/analysis/source_lock.py` — generate and validate `docs/reference/source-lock.json`.
- Create `tools/analysis/reconstruct_stock.py` — verify ordered split parts and reconstruct the original stock RAR atomically.
- Create `tests/analysis_test_utils.py` — ZIP and split-part fixtures shared by analysis tests.
- Create `tests/test_archive_inventory.py` — inventory behavior tests.
- Create `tests/test_tree_compare.py` — path/content comparison tests.
- Create `tests/test_source_lock.py` — source-lock generation and validation tests.
- Create `tests/test_reconstruct_stock.py` — split reconstruction, corruption, ordering, and atomicity tests.
- Create `docs/reference/archive-inventory.json` — generated compact metadata for all supplied ZIP archives.
- Create `docs/reference/archive-comparisons.json` — generated compact comparison facts.
- Create `docs/reference/full-artifacts.sha256` — hashes and Drive location for complete path-level reports.
- Create `docs/reference/README.md` — commands and interpretation rules.
- Create `docs/stock/h1a1000-r118/README.md` — exact stock-part naming, manifest, reconstruction, and verification contract.

---

### Task 1: ZIP Archive Inventory

**Files:**
- Create: `tests/analysis_test_utils.py`
- Create: `tests/test_archive_inventory.py`
- Create: `tools/analysis/archive_inventory.py`

**Interfaces:**
- Produces: `inventory_zip(path: Path) -> dict[str, object]`
- Produces: `inventory_many(paths: Sequence[Path]) -> list[dict[str, object]]`
- Produces CLI: `python3 tools/analysis/archive_inventory.py --output <json> <zip>...`
- Output keys: `archive`, `archive_sha256`, `archive_size_bytes`, `embedded_source_commit`, `root_directory`, `file_count`, `uncompressed_size_bytes`, `files`.
- Each `files` item contains only `path`, `size_bytes`, `sha256`, and `zip_mode`.

- [ ] **Step 1: Add reusable ZIP fixture helper**

```python
# tests/analysis_test_utils.py
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def write_zip(path: Path, entries: dict[str, bytes], comment: str = "") -> Path:
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        archive.comment = comment.encode("utf-8")
        for name, payload in entries.items():
            archive.writestr(name, payload)
    return path
```

- [ ] **Step 2: Write a failing inventory normalization test**

```python
# tests/test_archive_inventory.py
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
```

- [ ] **Step 3: Run the test and verify RED**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_archive_inventory -v
```

Expected: import failure for `tools.analysis.archive_inventory` because the production module does not exist.

- [ ] **Step 4: Implement minimal deterministic inventory**

```python
# tools/analysis/archive_inventory.py
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence
from zipfile import ZipFile, ZipInfo


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_root(infos: list[ZipInfo]) -> str | None:
    roots = {info.filename.split("/", 1)[0] for info in infos if info.filename}
    return next(iter(roots)) if len(roots) == 1 else None


def inventory_zip(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        infos = [info for info in archive.infolist() if not info.is_dir()]
        root = normalized_root(infos)
        files = []
        for info in infos:
            relative = info.filename
            if root and relative.startswith(root + "/"):
                relative = relative[len(root) + 1 :]
            files.append(
                {
                    "path": relative,
                    "size_bytes": info.file_size,
                    "sha256": sha256_bytes(archive.read(info)),
                    "zip_mode": (info.external_attr >> 16) & 0xFFFF,
                }
            )
        files.sort(key=lambda item: str(item["path"]))
        return {
            "archive": path.name,
            "archive_sha256": sha256_file(path),
            "archive_size_bytes": path.stat().st_size,
            "embedded_source_commit": archive.comment.decode("utf-8", "replace").strip() or None,
            "root_directory": root,
            "file_count": len(files),
            "uncompressed_size_bytes": sum(int(item["size_bytes"]) for item in files),
            "files": files,
        }


def inventory_many(paths: Sequence[Path]) -> list[dict[str, object]]:
    return [inventory_zip(path) for path in sorted(paths, key=lambda value: value.name)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archives", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = inventory_many(args.archives)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run the focused test and verify GREEN**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_archive_inventory -v
```

Expected: `1 test ... OK`.

- [ ] **Step 6: Add edge-case tests**

Add tests proving that multiple archive roots result in `root_directory = None`, directory entries are omitted, empty files are retained, and repeated runs produce byte-identical JSON.

- [ ] **Step 7: Run all archive inventory tests**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_archive_inventory -v
```

Expected: all archive inventory tests pass with no warnings.

- [ ] **Step 8: Commit**

```bash
git add tools/analysis/archive_inventory.py tests/analysis_test_utils.py tests/test_archive_inventory.py
git commit -m "tools: add deterministic reference archive inventory"
```

### Task 2: Normalized Tree Comparison

**Files:**
- Create: `tests/test_tree_compare.py`
- Create: `tools/analysis/tree_compare.py`

**Interfaces:**
- Consumes: inventory dictionaries produced by `inventory_zip`.
- Produces: `compare_inventories(left: dict, right: dict) -> dict[str, object]`.
- Produces CLI: `python3 tools/analysis/tree_compare.py --inventory <json> --pair <left>:<right> --output <json>`.
- Output keys: `left`, `right`, `left_files`, `right_files`, `common_paths`, `identical_common_paths`, `different_common_paths`, `left_only_paths`, `right_only_paths`, `identical_paths`, `different_paths`.

- [ ] **Step 1: Write a failing comparison test**

```python
# tests/test_tree_compare.py
import unittest

from tools.analysis.tree_compare import compare_inventories


class TreeCompareTest(unittest.TestCase):
    def test_distinguishes_identical_changed_and_unique_paths(self) -> None:
        left = {
            "archive": "left.zip",
            "files": [
                {"path": "same", "sha256": "a"},
                {"path": "changed", "sha256": "b"},
                {"path": "left-only", "sha256": "c"},
            ],
        }
        right = {
            "archive": "right.zip",
            "files": [
                {"path": "same", "sha256": "a"},
                {"path": "changed", "sha256": "x"},
                {"path": "right-only", "sha256": "y"},
            ],
        }

        result = compare_inventories(left, right)

        self.assertEqual(result["identical_paths"], ["same"])
        self.assertEqual(result["different_paths"], ["changed"])
        self.assertEqual(result["left_only_paths"], ["left-only"])
        self.assertEqual(result["right_only_paths"], ["right-only"])
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_tree_compare -v
```

Expected: import failure for `tools.analysis.tree_compare`.

- [ ] **Step 3: Implement comparison using normalized path maps**

```python
# tools/analysis/tree_compare.py
from __future__ import annotations


def compare_inventories(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    left_map = {str(item["path"]): str(item["sha256"]) for item in left["files"]}
    right_map = {str(item["path"]): str(item["sha256"]) for item in right["files"]}
    common = set(left_map) & set(right_map)
    identical = sorted(path for path in common if left_map[path] == right_map[path])
    different = sorted(common - set(identical))
    left_only = sorted(set(left_map) - set(right_map))
    right_only = sorted(set(right_map) - set(left_map))
    return {
        "left": left["archive"],
        "right": right["archive"],
        "left_files": len(left_map),
        "right_files": len(right_map),
        "common_paths": len(common),
        "identical_common_paths": len(identical),
        "different_common_paths": len(different),
        "left_only_paths": left_only,
        "right_only_paths": right_only,
        "identical_paths": identical,
        "different_paths": different,
    }
```

Add argument parsing that loads one inventory file, resolves archive names exactly, rejects unknown names, supports repeated `--pair`, sorts pair results, and writes stable JSON.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_tree_compare -v
```

Expected: all comparison tests pass.

- [ ] **Step 5: Commit**

```bash
git add tools/analysis/tree_compare.py tests/test_tree_compare.py
git commit -m "tools: compare normalized device and vendor trees"
```

### Task 3: Source-Lock Generation and Validation

**Files:**
- Create: `tests/test_source_lock.py`
- Create: `tools/analysis/source_lock.py`
- Modify: `docs/reference/source-lock.json`

**Interfaces:**
- Consumes: compact archive inventory generated by Task 1.
- Produces: `validate_source_lock(lock: dict, inventory: list[dict]) -> list[str]`.
- Produces CLI modes:
  - `--validate --lock docs/reference/source-lock.json --inventory docs/reference/archive-inventory.json`
  - `--write-reference-section --lock ... --inventory ...`
- Validation compares archive name, archive SHA-256, archive size, uncompressed size, file count, root directory, and embedded commit.

- [ ] **Step 1: Write a failing mismatch test**

```python
# tests/test_source_lock.py
import unittest

from tools.analysis.source_lock import validate_source_lock


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
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_source_lock -v
```

Expected: import failure for `tools.analysis.source_lock`.

- [ ] **Step 3: Implement exact validation**

Implement one archive-name map per input, reject duplicate archive names, report missing and unexpected archives, and compare these field mappings:

```python
FIELD_MAP = {
    "sha256": "archive_sha256",
    "archive_size_bytes": "archive_size_bytes",
    "uncompressed_size_bytes": "uncompressed_size_bytes",
    "file_count": "file_count",
    "root_directory": "root_directory",
    "embedded_source_commit": "embedded_source_commit",
}
```

The CLI exits `0` with `source lock verified: N archives` when no errors exist and exits `1` after printing every mismatch otherwise.

- [ ] **Step 4: Run tests and verify GREEN**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_source_lock -v
```

Expected: all source-lock tests pass.

- [ ] **Step 5: Generate inventory from the supplied archives**

Run from a workspace where the supplied ZIP files are mounted under `/mnt/data`:

```bash
python3 tools/analysis/archive_inventory.py \
  --output docs/reference/archive-inventory.json \
  /mnt/data/android_device_*.zip \
  /mnt/data/proprietary_vendor_*.zip \
  /mnt/data/device_red_hydrogenone*.zip
```

Expected: 13 archive records sorted by filename.

- [ ] **Step 6: Validate the checked-in source lock**

Run:

```bash
python3 tools/analysis/source_lock.py \
  --validate \
  --lock docs/reference/source-lock.json \
  --inventory docs/reference/archive-inventory.json
```

Expected: `source lock verified: 13 archives` and exit `0`.

- [ ] **Step 7: Commit**

```bash
git add tools/analysis/source_lock.py tests/test_source_lock.py docs/reference/source-lock.json docs/reference/archive-inventory.json
git commit -m "tools: validate locked donor archive inputs"
```

### Task 4: Generate and Review Donor Comparisons

**Files:**
- Create: `docs/reference/archive-comparisons.json`
- Create: `docs/reference/README.md`

**Interfaces:**
- Consumes: `docs/reference/archive-inventory.json`.
- Produces exact comparisons for:
  - current Hydrogen One versus the second supplied Hydrogen One archive;
  - current Hydrogen One versus mata;
  - current Hydrogen One versus OnePlus MSM8998 common;
  - current Hydrogen One versus Nubia MSM8998 common;
  - OnePlus MSM8998 common versus Nubia MSM8998 common;
  - each donor device tree versus its manufacturer common tree;
  - each donor vendor device tree versus its manufacturer common vendor tree where both were supplied.

- [ ] **Step 1: Generate comparison JSON**

Run the CLI with explicit repeated pairs. Do not use filename heuristics inside the tool.

Expected locked headline results:

```text
Hydrogen main vs Hydrogen runtime-contract: 423 common, 423 identical
Hydrogen main vs mata: 299 common, 253 identical, 46 different
Hydrogen main vs OnePlus common: 50 common, 3 identical, 47 different
Hydrogen main vs Nubia common: 139 common, 22 identical, 117 different
OnePlus common vs Nubia common: 59 common, 8 identical, 51 different
```

- [ ] **Step 2: Verify generated JSON is deterministic**

Run the generation command twice and compare:

```bash
sha256sum docs/reference/archive-comparisons.json
cp docs/reference/archive-comparisons.json /tmp/archive-comparisons.first.json
# rerun generation
cmp /tmp/archive-comparisons.first.json docs/reference/archive-comparisons.json
```

Expected: `cmp` exits `0`.

- [ ] **Step 3: Document interpretation rules**

`docs/reference/README.md` must state:

- a matching path is not proof of compatibility;
- byte-identical platform files still require RED stock confirmation when they encode hardware paths, properties, services, or permissions;
- vendor blobs are never copied from donors solely because their `DT_NEEDED` graph resolves;
- common-tree paths are flattened only after subsystem classification;
- large generated inventories contain hashes and metadata, never proprietary file contents.

- [ ] **Step 4: Commit**

```bash
git add docs/reference/archive-comparisons.json docs/reference/README.md
git commit -m "docs: record normalized MSM8998 donor comparisons"
```

### Task 5: Verified Reconstruction of Split Stock Archive

**Files:**
- Create: `tests/test_reconstruct_stock.py`
- Create: `tools/analysis/reconstruct_stock.py`
- Create: `docs/stock/h1a1000-r118/README.md`

**Interfaces:**
- Manifest format: one line per part, exactly `<sha256><two spaces><filename>`, UTF-8, LF.
- Produces: `reconstruct(parts_dir: Path, manifest_path: Path, output_path: Path, expected_sha256: str) -> None`.
- CLI: `python3 tools/analysis/reconstruct_stock.py --parts-dir <dir> --manifest <parts.sha256> --output <rar> --expected-sha256 <digest>`.
- Reconstruction writes `<output>.partial`, fsyncs, verifies final SHA-256, then atomically replaces `<output>`.

- [ ] **Step 1: Write failing successful-reconstruction test**

```python
# tests/test_reconstruct_stock.py
import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.analysis.reconstruct_stock import reconstruct


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
```

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_reconstruct_stock -v
```

Expected: import failure for `tools.analysis.reconstruct_stock`.

- [ ] **Step 3: Implement strict manifest parsing and atomic reconstruction**

Implementation requirements:

- reject malformed hashes and filenames containing `/`, `\\`, or `..` path segments;
- reject duplicate part names;
- reject missing and hash-mismatched parts before creating the partial output;
- concatenate in manifest order, not glob order;
- remove the partial file on any exception;
- reject an existing output unless `--replace` is explicitly provided;
- verify final SHA-256 before `Path.replace`.

- [ ] **Step 4: Add corruption and atomicity tests**

Add tests proving:

- one corrupt part raises `ValueError` naming that part;
- a wrong final hash raises `ValueError` and leaves no final/partial file;
- manifest order controls concatenation;
- a path traversal filename is rejected;
- an existing final file is preserved when replacement is not enabled.

- [ ] **Step 5: Run reconstruction tests and verify GREEN**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest tests.test_reconstruct_stock -v
```

Expected: all reconstruction tests pass.

- [ ] **Step 6: Write stock intake documentation**

`docs/stock/h1a1000-r118/README.md` records:

```text
archive: [FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar
Drive-reported size: 1851974911 bytes
part maximum: 240 MiB
part pattern: H1A1000_r118.rar.00.part, .01.part, ...
required manifests: parts.sha256 and original.sha256
```

It also gives the exact reconstruction command and requires `7z t` plus SHA-256 verification before extraction.

- [ ] **Step 7: Commit**

```bash
git add tools/analysis/reconstruct_stock.py tests/test_reconstruct_stock.py docs/stock/h1a1000-r118/README.md
git commit -m "tools: verify and reconstruct split stock 118 archive"
```

### Task 6: Full Verification and Handoff to Stock Extraction Plan

**Files:**
- Modify: `tests/test_full_tree.py`
- Modify: `docs/reference/README.md`

**Interfaces:**
- Existing tree test gains checks that the approved design, source lock, generated inventory, comparisons, and stock intake documentation exist.
- Source-lock validation remains the authoritative content check.

- [ ] **Step 1: Write failing repository-contract assertions**

Add assertions to `tests/test_full_tree.py` for these paths:

```python
required_analysis_files = [
    "docs/superpowers/specs/2026-09-02-hydrogenone-lineage22.2-design.md",
    "docs/reference/SUPPLIED_SOURCES.md",
    "docs/reference/source-lock.json",
    "docs/reference/archive-inventory.json",
    "docs/reference/archive-comparisons.json",
    "docs/reference/README.md",
    "docs/stock/h1a1000-r118/README.md",
]
```

The test must also reject an actual directory named `device/red/msm8998-common` or an include/reference to that path in Hydrogen One makefiles.

- [ ] **Step 2: Run repository test and verify RED**

Run:

```bash
python3 tests/test_full_tree.py
```

Expected: failure because generated analysis files are not all present before Tasks 1–5 complete.

- [ ] **Step 3: Complete missing generated artifacts and rerun all tests**

Run:

```bash
PYTHONPATH=tests:. python3 -m unittest \
  tests.test_archive_inventory \
  tests.test_tree_compare \
  tests.test_source_lock \
  tests.test_reconstruct_stock -v
python3 tests/test_full_tree.py
python3 tools/analysis/source_lock.py \
  --validate \
  --lock docs/reference/source-lock.json \
  --inventory docs/reference/archive-inventory.json
```

Expected:

- all unit tests report `OK`;
- `tests/test_full_tree.py` exits `0`;
- source-lock validation prints `source lock verified: 13 archives` and exits `0`.

- [ ] **Step 4: Confirm branch diff is documentation/tooling only**

Run:

```bash
git diff --stat main...HEAD
git diff --name-only main...HEAD
```

Expected: only `docs/`, `tools/analysis/`, and `tests/` paths. No production `BoardConfig.mk`, `device.mk`, VINTF, init, SELinux, or proprietary-list changes occur before verified `.118` stock extraction.

- [ ] **Step 5: Commit**

```bash
git add tests/test_full_tree.py docs/reference/README.md
git commit -m "tests: enforce reference-analysis contract"
```

- [ ] **Step 6: Create the next plan only after stock reconstruction succeeds**

The next implementation plan is `docs/superpowers/plans/2026-09-02-hydrogenone-stock118-extraction.md`. Its entry evidence is:

- verified reconstructed RAR SHA-256;
- successful `7z t` output;
- extracted package file list and hashes;
- confirmed build properties showing the actual Android release and build identity.

That plan covers fastboot package parsing, sparse image conversion, partition/boot analysis, filesystem inventory, ELF dependency graphs, init/VINTF/SELinux mapping, and runtime collector integration. It must not assume Android 9 solely from the filename.
