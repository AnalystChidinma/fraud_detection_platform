from pathlib import Path


class FileValidator:
    """
    Validate an incoming file before it enters the ingestion pipeline.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def file_exists(self):
        """Check whether the file exists."""
        return self.file_path.is_file()

    def is_csv(self):
        """Check whether the file has a CSV extension."""
        return self.file_path.suffix.lower() == ".csv"

    def is_empty(self):
        """Check whether the file is empty."""
        return self.file_path.stat().st_size == 0

    def validate(self):
        """
        Run all validation checks.

        Returns:
            bool: True if all validations pass.
        """
        return (
            self.file_exists()
            and self.is_csv()
            and not self.is_empty()
        )
