"""
Centralized application configuration for the Fraud Detection project.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv


# Project root:
# Fraud_detection/
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the root project .env file explicitly.
load_dotenv(BASE_DIR / ".env")


# Logging configuration
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "fraud_detection.log")
LOG_LEVEL = getattr(
    logging,
    os.getenv("LOG_LEVEL", "INFO").upper(),
    logging.INFO,
)


class Settings:
    """Application configuration loaded from environment variables."""

    # AWS S3 settings
    AWS_PROFILE = os.getenv("AWS_PROFILE", "fraud-project")
    AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
    AWS_S3_BUCKET = os.getenv(
        "AWS_S3_BUCKET",
        "fraud-detection-raw-chidinma-2026",
    )
    # ADD THIS LINE: Reads endpoint configuration for local MinIO compatibility
    AWS_ENDPOINT_URL = os.getenv("LOCAL_MINIO_ENDPOINT")


    # Snowflake settings
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")


    @classmethod
    def validate_s3_settings(cls) -> None:
        """Validate the required AWS S3 configuration."""

        required_values = {
            "AWS_PROFILE": cls.AWS_PROFILE,
            "AWS_REGION": cls.AWS_REGION,
            "AWS_S3_BUCKET": cls.AWS_S3_BUCKET,
        }

        missing_values = [
            name
            for name, value in required_values.items()
            if not value
        ]

        if missing_values:
            raise ValueError(
                "Missing required AWS S3 configuration: "
                + ", ".join(missing_values)
            )

