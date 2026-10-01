import os

import snowflake.connector
from dotenv import load_dotenv


load_dotenv()


class SnowflakeClient:
    """Create and manage a connection to Snowflake."""

    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = os.getenv("SNOWFLAKE_USER")
        self.password = os.getenv("SNOWFLAKE_PASSWORD")
        self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
        self.database = os.getenv("SNOWFLAKE_DATABASE")
        self.schema = os.getenv("SNOWFLAKE_SCHEMA")

        self._validate_configuration()

    def _validate_configuration(self):
        required = {
            "SNOWFLAKE_ACCOUNT": self.account,
            "SNOWFLAKE_USER": self.user,
            "SNOWFLAKE_PASSWORD": self.password,
            "SNOWFLAKE_WAREHOUSE": self.warehouse,
            "SNOWFLAKE_DATABASE": self.database,
            "SNOWFLAKE_SCHEMA": self.schema,
        }

        missing = [
            name
            for name, value in required.items()
            if not value
        ]

        if missing:
            raise ValueError(
                f"Missing Snowflake configuration: {', '.join(missing)}"
            )

    def connect(self):
        """Create and return a Snowflake connection."""

        return snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
        )