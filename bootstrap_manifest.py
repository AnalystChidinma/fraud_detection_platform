from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError

from ingestion.checksum import calculate_sha256
from ingestion.config import Settings
from ingestion.logger import get_logger
from ingestion.manifest import IngestionManifest
from ingestion.s3_client import get_s3_client


logger = get_logger(__name__)


BATCH_DIRECTORY = Path("data/batches")


if __name__ == "__main__":

    manifest = IngestionManifest()
    client = get_s3_client()

    registered = 0

    for batch_file in sorted(BATCH_DIRECTORY.glob("*.csv")):

        object_name = (
            f"raw/paysim/transactions/batches/{batch_file.name}"
        )

        try:
            client.head_object(
                Bucket=Settings.AWS_S3_BUCKET,
                Key=object_name,
            )

        except ClientError:
            logger.warning(
                "Batch not found in AWS S3: %s",
                batch_file.name,
            )
            continue

        except BotoCoreError:
            logger.exception(
                "AWS S3 error while checking batch: %s",
                batch_file.name,
            )
            raise

        checksum = calculate_sha256(batch_file)

        manifest.record_success(
            file_name=batch_file.name,
            checksum=checksum,
            file_size=batch_file.stat().st_size,
            object_name=object_name,
        )

        registered += 1

    logger.info(
        "Registered %s existing batches in the ingestion manifest.",
        registered,
    )