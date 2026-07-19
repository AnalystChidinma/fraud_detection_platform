"""
Application configuration.

This module centralizes all configuration used throughout the
fraud detection ingestion pipeline.

Environment-specific values are loaded from the .env file,
while project paths and application constants are defined here.

"""

from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
ARCHIVE_DIR = DATA_DIR / "archive"
SAMPLE_DIR = DATA_DIR / "sample"

LOG_DIR = PROJECT_ROOT / "logs"



AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_RAW_PREFIX = os.getenv("S3_RAW_PREFIX")
S3_ARCHIVE_PREFIX = os.getenv("S3_ARCHIVE_PREFIX")



LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_NAME = "ingestion.log"


SUPPORTED_FILE_TYPES = (".csv")