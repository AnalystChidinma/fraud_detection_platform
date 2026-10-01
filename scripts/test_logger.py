from ingestion.logger import get_logger

logger = get_logger(__name__)

logger.info("Logger initialized successfully.")
logger.warning("This is a warning message.")
logger.error("This is a test error.")

