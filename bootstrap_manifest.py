from pathlib import Path

from ingestion.checksum import calculate_sha256
from ingestion.manifest import IngestionManifest
from ingestion.minio_client import get_minio_client
from ingestion.config import Settings


BATCH_DIRECTORY = Path("data/batches")


if __name__ == "__main__":

    manifest = IngestionManifest()
    client = get_minio_client()

    registered = 0

    for batch_file in sorted(BATCH_DIRECTORY.glob("*.csv")):

        object_name = (
            f"transactions/batches/{batch_file.name}"
        )

        try:
            client.stat_object(
                Settings.MINIO_RAW_BUCKET,
                object_name,
            )

        except Exception:
            print(
                f"Not found in MinIO: {batch_file.name}"
            )
            continue

        checksum = calculate_sha256(batch_file)

        manifest.record_success(
            file_name=batch_file.name,
            checksum=checksum,
            file_size=batch_file.stat().st_size,
            object_name=object_name,
        )

        registered += 1

    print(
        f"Registered {registered} existing batches "
        "in the ingestion manifest."
    )