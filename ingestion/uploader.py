"""
Upload validated source files to the AWS S3 raw landing zone.
"""

from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError

from ingestion.checksum import calculate_sha256
from ingestion.config import Settings
from ingestion.logger import get_logger
from ingestion.s3_client import get_s3_client
from ingestion.validator import FileValidator


logger = get_logger(__name__)


class RawFileUploader:
    """Upload original source files to the AWS S3 raw bucket."""

    def __init__(self) -> None:
        self.client = get_s3_client()
        self.bucket_name = Settings.AWS_S3_BUCKET

    def upload(
        self,
        file_path: str | Path,
        object_name: str | None = None,
    ) -> dict[str, str | int]:
        """
        Validate and upload a source CSV file to AWS S3.

        Args:
            file_path: Local source file path.
            object_name: Optional destination object name.

        Returns:
            Upload metadata.

        Raises:
            ValueError: If validation fails.
            ClientError: If AWS S3 rejects the upload.
            BotoCoreError: If the AWS SDK encounters an error.
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
            else f"raw/paysim/transactions/{path.name}"
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
            self.client.upload_file(
                Filename=str(path),
                Bucket=self.bucket_name,
                Key=destination_name,
                ExtraArgs={
                    "ContentType": "text/csv",
                    "Metadata": {
                        "sha256": checksum,
                        "source-filename": path.name,
                    },
                },
            )

        except (ClientError, BotoCoreError):
            logger.exception(
                "AWS S3 upload failed. File=%s",
                path,
            )
            raise

        logger.info(
            "Upload completed. Bucket=%s Object=%s",
            self.bucket_name,
            destination_name,
        )

        return {
            "bucket_name": self.bucket_name,
            "object_name": destination_name,
            "checksum": checksum,
            "file_size": file_size,
        }
