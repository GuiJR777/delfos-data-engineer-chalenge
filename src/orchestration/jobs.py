# Jobs do Dagster.

from dagster import AssetSelection, JobDefinition, define_asset_job

from orchestration.constants import ETL_ASSET_NAME, ETL_JOB_NAME


class DailyEtlJobFactory:
    def get_job(self) -> JobDefinition:
        selection = AssetSelection.assets(ETL_ASSET_NAME)
        return define_asset_job(
            name=ETL_JOB_NAME,
            selection=selection,
        )
