"""
Snowflake loading utilities for the FinGuard pipeline.
"""

from ingestion.logger import get_logger
from ingestion.snowflake_client import SnowflakeClient

logger = get_logger(__name__)


class SnowflakeLoader:
    """Load transaction files from the S3-backed Snowflake stage."""

    def __init__(self) -> None:
        self.client = SnowflakeClient()

    def load_transactions(self) -> None:
        """Load new transaction files from the S3 stage into RAW.TRANSACTIONS."""

        copy_sql = """
        COPY INTO FRAUD_ANALYTICS.RAW.TRANSACTIONS
        FROM @FRAUD_ANALYTICS.RAW.PAYSIM_STAGE
        FILE_FORMAT = (
            TYPE = CSV
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        )
        PATTERN = '.*transactions_batch_.*\\.csv';
        """


        logger.info("Starting Snowflake transaction load.")

        connection = self.client.connect()

       
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(copy_sql)

                results = cursor.fetchall()

                logger.info(
                    "Snowflake transaction load completed. Result=%s",
                    results[0][0],
                )

                return results
            
            except Exception:
                logger.exception("Snowflake transaction load failed.")
                raise

            finally:
                cursor.close()

        finally:
            connection.close()
