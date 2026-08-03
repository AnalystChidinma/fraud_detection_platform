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
LOG_DIR = BASE_DIR / "logs"
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "fraud_detection.log")
LOG_LEVEL = getattr(
    logging,
    os.getenv("LOG_LEVEL", "INFO").upper(),
    logging.INFO,
)


class Settings:
    """Application configuration loaded from environment variables."""

    # MinIO connection settings
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

    # MinIO bucket names
    MINIO_RAW_BUCKET = os.getenv("MINIO_RAW_BUCKET", "raw")
    MINIO_PROCESSED_BUCKET = os.getenv(
        "MINIO_PROCESSED_BUCKET",
        "processed",
    )
    MINIO_ARCHIVE_BUCKET = os.getenv(
        "MINIO_ARCHIVE_BUCKET",
        "archive",
    )

    @classmethod
    def validate_minio_settings(cls) -> None:
        """Validate the required MinIO environment variables."""

        required_values = {
            "MINIO_ACCESS_KEY": cls.MINIO_ACCESS_KEY,
            "MINIO_SECRET_KEY": cls.MINIO_SECRET_KEY,
        }

        missing_values = [
            name
            for name, value in required_values.items()
            if not value
        ]

        if missing_values:
            raise ValueError(
                "Missing required environment variables: "
                + ", ".join(missing_values)
            )