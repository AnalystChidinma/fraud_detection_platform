"""
Upload validated source files to the MinIO raw landing zone.
"""

from pathlib import Path

from minio.error import S3Error

from ingestion.checksum import calculate_sha256
from ingestion.config import Settings
from ingestion.logger import get_logger
from ingestion.minio_client import get_minio_client
from ingestion.validator import FileValidator


logger = get_logger(__name__)


class RawFileUploader:
    """Upload original source files to the MinIO raw bucket."""

    def __init__(self) -> None:
        self.client = get_minio_client()
        self.bucket_name = Settings.MINIO_RAW_BUCKET

    def upload(
        self,
        file_path: str | Path,
        object_name: str | None = None,
    ) -> dict[str, str | int]:
        """
        Validate and upload a source CSV file to MinIO.

        Args:
            file_path: Local source file path.
            object_name: Optional destination object name.

        Returns:
            Upload metadata.

        Raises:
            ValueError: If validation fails.
            S3Error: If MinIO rejects the upload.
        """
        path = Path(file_path)
        validator = FileValidator(path)

        if not validator.validate():
            raise ValueError(f"File failed validation: {path}")

        checksum = calculate_sha256(path)
        file_size = path.stat().st_size

        destination_name = (
            object_name
            if object_name
            else f"transactions/{path.name}"
        )

        logger.info(
            "Uploading file. Source=%s Bucket=%s Object=%s Size=%s Checksum=%s",
            path,
            self.bucket_name,
            destination_name,
            file_size,
            checksum,
        )

        try:
            result = self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=destination_name,
                file_path=str(path),
                content_type="text/csv",
                metadata={
                    "sha256": checksum,
                    "source-filename": path.name,
                },
            )

        except S3Error:
            logger.exception("MinIO upload failed. File=%s", path)
            raise

        logger.info(
            "Upload completed. Bucket=%s Object=%s Version=%s",
            result.bucket_name,
            result.object_name,
            result.version_id,
        )

        return {
            "bucket_name": result.bucket_name,
            "object_name": result.object_name,
            "checksum": checksum,
            "file_size": file_size,
        }