# Asset do ETL diario.

from datetime import date

from dagster import AssetExecutionContext, DailyPartitionsDefinition, asset

from etl.run import run_daily_etl
from etl.source_api_client import SourceApiClient
from etl.target_database.database import TargetDatabaseEngineManager
from orchestration.constants import (
    ETL_ASSET_NAME,
    PARTITION_START_DATE,
    SOURCE_API_RESOURCE_KEY,
    TARGET_DB_ENGINE_RESOURCE_KEY,
)

DAILY_PARTITIONS = DailyPartitionsDefinition(
    start_date=PARTITION_START_DATE,
)


class DailyEtlAssetExecutor:
    def __init__(
        self,
        api_client: SourceApiClient,
        engine_manager: TargetDatabaseEngineManager,
    ) -> None:
        self._api_client = api_client
        self._engine_manager = engine_manager

    def do_materialize(self, context: AssetExecutionContext) -> int:
        target_date = self._get_target_date(context.partition_key)
        return run_daily_etl(
            target_date=target_date,
            api_client=self._api_client,
            engine_manager=self._engine_manager,
        )

    def _get_target_date(self, partition_key: str) -> date:
        return date.fromisoformat(partition_key)


@asset(
    name=ETL_ASSET_NAME,
    partitions_def=DAILY_PARTITIONS,
    required_resource_keys={
        SOURCE_API_RESOURCE_KEY,
        TARGET_DB_ENGINE_RESOURCE_KEY,
    },
)
def daily_etl_asset(context: AssetExecutionContext) -> int:
    executor = DailyEtlAssetExecutor(
        api_client=context.resources.source_api_client,
        engine_manager=context.resources.target_db_engine,
    )
    return executor.do_materialize(context)

