# Constantes do Dagster.

PARTITION_START_DATE: str = "2024-01-01"
DAILY_SCHEDULE_CRON: str = "0 1 * * *"

ETL_ASSET_NAME: str = "daily_etl"
ETL_JOB_NAME: str = "daily_etl_job"
ETL_SCHEDULE_NAME: str = "daily_etl_schedule"

SOURCE_API_RESOURCE_KEY: str = "source_api_client"
TARGET_DB_ENGINE_RESOURCE_KEY: str = "target_db_engine"

