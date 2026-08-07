from ingestion.uploader import RawFileUploader


if __name__ == "__main__":
    uploader = RawFileUploader()

    result = uploader.upload(
        "data/sample/paysim_sample.csv"
    )

    print(result)