from ingestion.snowflake_client import SnowflakeClient


def test_snowflake_connection():
    client = SnowflakeClient()

    connection = client.connect()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")

        result = cursor.fetchone()

        assert result[0] == "FRAUD_ANALYTICS"
        assert result[1] == "RAW"

    finally:
        connection.close()