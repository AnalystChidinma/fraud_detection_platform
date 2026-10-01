from ingestion.batch_loader import BatchLoader


if __name__ == "__main__":
    loader = BatchLoader(
        source_file="data/raw/paysim_transactions.csv",
        batch_directory="data/batches",
        batch_size=100_000,
    )

    results = loader.run()

    print(f"Successfully uploaded {len(results)} batches.")