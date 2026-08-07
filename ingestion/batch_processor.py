from pathlib import Path

import polars as pl

from ingestion.logger import get_logger


logger = get_logger(__name__)


class BatchProcessor:

    """Split a large CSV source file into smaller CSV batch files."""

    def __init__(
        self,
        source_file: str | Path,
        output_dir: str | Path,
        batch_size: int = 100_000,
    ) -> None:
        self.source_file = Path(source_file)
        self.output_dir = Path(output_dir)
        self.batch_size = batch_size

    def process(self) -> list[Path]:
        """
        Split the source CSV into smaller CSV batch files.

        Returns:
            list[Path]: Paths of generated batch files.
        """
        if not self.source_file.is_file():
            raise FileNotFoundError(
                f"Source file not found: {self.source_file}"
            )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Starting batch processing. Source=%s BatchSize=%s",
            self.source_file,
            self.batch_size,
        )

        dataframe = pl.read_csv(self.source_file)

        total_rows = dataframe.height

        logger.info(
            "Source file loaded. TotalRows=%s",
            total_rows,
        )

        generated_batches: list[Path] = []

        batch_number = 1

        for start_row in range(
            0,
            total_rows,
            self.batch_size,
        ):
            batch = dataframe.slice(
                start_row,
                self.batch_size,
            )

            batch_file = (
                self.output_dir
                / f"transactions_batch_{batch_number:04d}.csv"
            )

            batch.write_csv(batch_file)

            generated_batches.append(batch_file)

            logger.info(
                "Batch created. Batch=%s Rows=%s File=%s",
                batch_number,
                batch.height,
                batch_file,
            )

            batch_number += 1

        logger.info(
            "Batch processing completed. TotalBatches=%s",
            len(generated_batches),
        )

        return generated_batches