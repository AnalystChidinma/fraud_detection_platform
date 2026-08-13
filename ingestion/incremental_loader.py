"""
Incremental batch ingestion for the Fraud Detection platform.

Only batches that have not been successfully processed before
are uploaded to the MinIO raw landing zone.
"""

from pathlib import Path

from ingestion.checksum import calculate_sha256
from ingestion.logger import get_logger
from ingestion.manifest import IngestionManifest
from ingestion.uploader import RawFileUploader


logger = get_logger(__name__)


class IncrementalLoader:
    """Upload only transaction batches that have not been processed."""

    def __init__(
        self,
        batch_directory: str | Path,
    ) -> None:
        self.batch_directory = Path(batch_directory)

        self.manifest = IngestionManifest()
        self.uploader = RawFileUploader()

    def run(self) -> dict[str, int]:
        """
        Process new batches while skipping previously completed batches.

        Returns:
            Dictionary containing uploaded and skipped batch counts.
        """

        if not self.batch_directory.is_dir():
            raise FileNotFoundError(
                f"Batch directory not found: {self.batch_directory}"
            )

        batch_files = sorted(
            self.batch_directory.glob("*.csv")
        )

        uploaded_count = 0
        skipped_count = 0

        logger.info(
            "Starting incremental ingestion. TotalBatches=%s",
            len(batch_files),
        )

        for batch_file in batch_files:

            checksum = calculate_sha256(batch_file)

            if self.manifest.is_processed(checksum):
                logger.info(
                    "Skipping already processed batch. File=%s",
                    batch_file.name,
                )

                skipped_count += 1
                continue

            object_name = (
                f"transactions/batches/{batch_file.name}"
            )

            result = self.uploader.upload(
                file_path=batch_file,
                object_name=object_name,
            )

            self.manifest.record_success(
                file_name=batch_file.name,
                checksum=checksum,
                file_size=result["file_size"],
                object_name=result["object_name"],
            )

            uploaded_count += 1

        logger.info(
            "Incremental ingestion completed. "
            "Uploaded=%s Skipped=%s",
            uploaded_count,
            skipped_count,
        )

        return {
            "uploaded": uploaded_count,
            "skipped": skipped_count,
        }