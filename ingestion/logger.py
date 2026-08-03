"""
Centralized logging configuration for the Fraud Detection project.

This module creates a reusable logger that writes log messages
to both the console and a log file.
"""

import logging
from pathlib import Path

from ingestion.config import LOG_DIR, LOG_FILE_NAME, LOG_LEVEL


def get_logger(name: str):
    """
    Create and return a configured logger.

    Args:
        name (str): Name of the module requesting the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOG_DIR / LOG_FILE_NAME

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Write logs to file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Display logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger