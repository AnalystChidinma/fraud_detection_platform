import boto3

import os
from botocore.exceptions import BotoCoreError, ClientError

from ingestion.config import Settings
from ingestion.logger import get_logger


logger = get_logger(__name__)



def get_s3_client():
    """
    Create and return a configured AWS S3 client.

    Returns:
        boto3.client: Authenticated AWS S3 client.
    """
    Settings.validate_s3_settings()

    endpoint_url = getattr(Settings, "AWS_ENDPOINT_URL", None)

    # 1. Initialize session
    if endpoint_url:
        # Local MinIO: explicit keys, ignore the AWS profile
        session = boto3.Session(
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
            region_name=Settings.AWS_REGION,
        )
    else:
        # Real AWS: use the named profile
        session = boto3.Session(
            profile_name=Settings.AWS_PROFILE,
            region_name=Settings.AWS_REGION,
        )

    # 2. Smart check: Is this pointing to a local MinIO stack or HTTP fallback?
    is_local = False
    if endpoint_url:
        is_local = "localhost" in endpoint_url or "minio" in endpoint_url or endpoint_url.startswith("http://")

    # 3. Inject local dev flags dynamically if endpoint_url exists
    client_kwargs = {}
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url
        if is_local:
            client_kwargs["use_ssl"] = False
            client_kwargs["verify"] = False

    client = session.client("s3", **client_kwargs)

    return client


def verify_s3_connection():
    """
    Verify that the application can connect to AWS S3.

    Returns:
        bool: True when the connection succeeds.
    """

    try:
        client = get_s3_client()

        response = client.head_bucket(
            Bucket=Settings.AWS_S3_BUCKET
        )

        logger.info(
            "AWS S3 connection successful. Bucket: %s",
            Settings.AWS_S3_BUCKET,
        )

        return response["ResponseMetadata"]["HTTPStatusCode"] == 200

    except ClientError as error:
        logger.exception(
            "AWS S3 rejected the request: %s",
            error,
        )
        return False

    except BotoCoreError as error:
        logger.exception(
            "AWS SDK error while connecting to S3: %s",
            error,
        )
        return False

    except Exception as error:
        logger.exception(
            "Could not connect to AWS S3: %s",
            error,
        )
        return False
