"""
Ingestion manifest for tracking processed transaction batches.

The manifest provides file-level idempotency by recording
successfully processed files using their SHA-256 checksums.
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class IngestionManifest:
    """Track ingestion history using a local SQLite database."""

    def __init__(
        self,
        database_path: str | Path = "data/metadata/ingestion_manifest.db",
    ) -> None:
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        """Create a connection to the manifest database."""
        return sqlite3.connect(self.database_path)

    def _create_table(self) -> None:
        """Create the ingestion manifest table if it does not exist."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ingestion_manifest (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    checksum TEXT NOT NULL UNIQUE,
                    file_size INTEGER NOT NULL,
                    object_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    processed_at TEXT NOT NULL
                )
                """
            )

    def is_processed(self, checksum: str) -> bool:
        """
        Check whether a checksum has already been successfully processed.
        """

        with self._connect() as connection:
            record = connection.execute(
                """
                SELECT 1
                FROM ingestion_manifest
                WHERE checksum = ?
                  AND status = 'SUCCESS'
                LIMIT 1
                """,
                (checksum,),
            ).fetchone()

        return record is not None

    def record_success(
        self,
        file_name: str,
        checksum: str,
        file_size: int,
        object_name: str,
    ) -> None:
        """Record a successfully processed batch."""

        processed_at = datetime.now(timezone.utc).isoformat()

        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO ingestion_manifest (
                    file_name,
                    checksum,
                    file_size,
                    object_name,
                    status,
                    processed_at
                )
                VALUES (?, ?, ?, ?, 'SUCCESS', ?)
                """,
                (
                    file_name,
                    checksum,
                    file_size,
                    object_name,
                    processed_at,
                ),
            )