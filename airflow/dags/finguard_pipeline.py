"""
FinGuard data pipeline DAG.
"""

import subprocess

import pendulum

from airflow.sdk import dag, task
import ingestion


@dag(
    dag_id="finguard_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2026, 9, 1, tz="Africa/Lagos"),
    catchup=False,
    tags=["finguard", "data-engineering"],
)
def finguard_pipeline():

    @task
    def ingest_batches():
        from ingestion.incremental_loader import IncrementalLoader

        loader = IncrementalLoader(
            "/opt/finguard/data/batches"
        )

        return loader.run()

    @task
    def load_snowflake():
        from ingestion.snowflake_loader import SnowflakeLoader

        loader = SnowflakeLoader()

        return loader.load_transactions()

    @task
    def dbt_build():
        result = subprocess.run(
            [
                "dbt",
                "build",
                "--project-dir",
                "/opt/finguard/dbt/finguard",
                "--profiles-dir",
                "/home/airflow/.dbt",
                "--log-path",
                "/tmp/dbt-logs",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return "dbt build completed successfully"

    ingestion = ingest_batches()
    snowflake_load = load_snowflake()
    transformation = dbt_build()

    ingestion >> snowflake_load >> transformation


finguard_pipeline()