from ingestion.batch_processor import BatchProcessor


if __name__ == "__main__":
    processor = BatchProcessor(
        source_file="data/raw/paysim_transactions.csv",
        output_dir="data/batches",
        batch_size=100_000,
    )

    batches = processor.process()

    print(f"Created {len(batches)} batches.")