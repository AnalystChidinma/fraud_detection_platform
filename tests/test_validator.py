from ingestion.validator import FileValidator


def test_file_exists_returns_true_for_existing_file(tmp_path):
    # Arrange
    test_file = tmp_path / "transactions.csv"
    test_file.write_text(
        "transaction_id,amount\n1,500")

    validator = FileValidator(str(test_file))

    # Act
    result = validator.file_exists()

    # Assert
    assert result is True


def test_file_exists_returns_false_for_missing_file(tmp_path):
    # Arrange
    missing_file = tmp_path / "missing.csv"

    validator = FileValidator(str(missing_file))

    # Act
    result = validator.file_exists()

    # Assert
    assert result is False


def test_file_exists_returns_false_for_directory(tmp_path):
    # Arrange
    validator = FileValidator(str(tmp_path))

    # Act
    result = validator.file_exists()

    # Assert
    assert result is False