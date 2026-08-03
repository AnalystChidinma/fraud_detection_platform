from ingestion.minio_client import verify_minio_connection


def test_minio_connection():
    """Confirm that Python can connect to MinIO."""

    result = verify_minio_connection()

    assert result is True