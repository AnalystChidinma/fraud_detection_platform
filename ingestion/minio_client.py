from minio import Minio
from minio.error import S3Error

from ingestion.config import Settings
from ingestion.logger import get_logger


logger = get_logger(__name__)


def get_minio_client():
    """
    Create and return a configured MinIO client.

    Returns:
        Minio: Authenticated MinIO client.
    """

    Settings.validate_minio_settings()

    client = Minio(
        endpoint=Settings.MINIO_ENDPOINT,
        access_key=Settings.MINIO_ACCESS_KEY,
        secret_key=Settings.MINIO_SECRET_KEY,
        secure=Settings.MINIO_SECURE,
    )

    return client


def verify_minio_connection():
    """
    Verify that the application can connect to MinIO.

    Returns:
        bool: True when the connection succeeds.
    """

    try:
        client = get_minio_client()
        buckets = client.list_buckets()

        bucket_names = [bucket.name for bucket in buckets]

        logger.info(
            "MinIO connection successful. Buckets: %s",
            bucket_names,
        )

        return True

    except S3Error as error:
        logger.exception(
            "MinIO rejected the request: %s",
            error,
        )
        return False

    except Exception as error:
        logger.exception(
            "Could not connect to MinIO: %s",
            error,
        )
        return False