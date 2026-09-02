from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def write_zip(path: Path, entries: dict[str, bytes], comment: str = "") -> Path:
    """Create a deterministic-enough ZIP fixture for behavior tests."""
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        archive.comment = comment.encode("utf-8")
        for name, payload in entries.items():
            archive.writestr(name, payload)
    return path
