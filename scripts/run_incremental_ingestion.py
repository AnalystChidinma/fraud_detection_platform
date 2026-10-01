from ingestion.incremental_loader import IncrementalLoader


if __name__ == "__main__":

    loader = IncrementalLoader(
        batch_directory="data/batches",
    )

    result = loader.run()

    print(result)