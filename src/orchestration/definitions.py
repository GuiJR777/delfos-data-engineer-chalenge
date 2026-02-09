# Definicoes do Dagster.

from dagster import Definitions

from orchestration.assets.etl_asset import daily_etl_asset
from orchestration.constants import (
    SOURCE_API_RESOURCE_KEY,
    TARGET_DB_ENGINE_RESOURCE_KEY,
)
from orchestration.jobs import DailyEtlJobFactory
from orchestration.resources import (
    source_api_client_resource,
    target_db_engine_resource,
)
from orchestration.schedules import DailyEtlScheduleFactory


class DagsterDefinitionsFactory:
    def get_definitions(self) -> Definitions:
        job = DailyEtlJobFactory().get_job()
        schedule = DailyEtlScheduleFactory(job).get_schedule()
        return Definitions(
            assets=[daily_etl_asset],
            jobs=[job],
            schedules=[schedule],
            resources={
                SOURCE_API_RESOURCE_KEY: source_api_client_resource,
                TARGET_DB_ENGINE_RESOURCE_KEY: target_db_engine_resource,
            },
        )


definitions = DagsterDefinitionsFactory().get_definitions()
