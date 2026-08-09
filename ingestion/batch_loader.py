"""
Batch ingestion workflow for the Fraud Detection platform.

This module coordinates CSV batch creation and uploads each
generated batch to the MinIO raw landing zone.
"""

from pathlib import Path

from ingestion.batch_processor import BatchProcessor
from ingestion.logger import get_logger
from ingestion.uploader import RawFileUploader


logger = get_logger(__name__)


class BatchLoader:
    """Coordinate batch creation and raw MinIO ingestion."""

    def __init__(
        self,
        source_file: str | Path,
        batch_directory: str | Path,
        batch_size: int = 100_000,
    ) -> None:
        self.source_file = Path(source_file)
        self.batch_directory = Path(batch_directory)
        self.batch_size = batch_size

        self.processor = BatchProcessor(
            source_file=self.source_file,
            output_dir=self.batch_directory,
            batch_size=self.batch_size,
        )

        self.uploader = RawFileUploader()

    def run(self) -> list[dict[str, str | int]]:
        """
        Split the source dataset into batches and upload each batch.

        Returns:
            list[dict]: Metadata returned for every successful upload.
        """

        logger.info(
            "Starting batch ingestion. Source=%s BatchSize=%s",
            self.source_file,
            self.batch_size,
        )

        batch_files = self.processor.process()

        uploaded_batches = []

        for batch_file in batch_files:
            object_name = f"transactions/batches/{batch_file.name}"

            logger.info(
                "Uploading batch. File=%s Object=%s",
                batch_file,
                object_name,
            )

            upload_result = self.uploader.upload(
                file_path=batch_file,
                object_name=object_name,
            )

            uploaded_batches.append(upload_result)

        logger.info(
            "Batch ingestion completed. TotalUploaded=%s",
            len(uploaded_batches),
        )

        return uploaded_batches