"""
Checksum utilities for ingestion files.
"""

import hashlib
from pathlib import Path


def calculate_sha256(
    file_path: str | Path,
    chunk_size: int = 1024 * 1024,
) :
    """
    Calculate the SHA-256 checksum of a file.

    Args:
        file_path: Path to the source file.
        chunk_size: Number of bytes read per iteration.

    Returns:
        Hexadecimal SHA-256 checksum.

    Raises:
        FileNotFoundError: If the path is not an existing file.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    sha256 = hashlib.sha256()

    with path.open("rb") as source_file:
        while chunk := source_file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()