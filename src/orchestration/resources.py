# Resources do Dagster.

from dagster import resource

from etl.settings import EtlSettings
from etl.source_api_client import SourceApiClient
from etl.target_database.database import TargetDatabaseEngineManager
from etl.target_database.settings import TargetDatabaseSettings


class SourceApiClientResourceFactory:
    def __init__(self, settings: EtlSettings) -> None:
        self._settings = settings

    def get_client(self) -> SourceApiClient:
        return SourceApiClient(
            base_url=self._settings.get_api_base_url(),
            timeout_seconds=self._settings.get_api_timeout_seconds(),
            retry_attempts=self._settings.get_api_retry_attempts(),
            api_limit=self._settings.get_api_limit(),
            api_offset=self._settings.get_api_offset(),
        )


class TargetDatabaseEngineResourceFactory:
    def __init__(self, settings: TargetDatabaseSettings) -> None:
        self._settings = settings

    def get_engine_manager(self) -> TargetDatabaseEngineManager:
        return TargetDatabaseEngineManager(self._settings)


@resource
def source_api_client_resource(_) -> SourceApiClient:
    settings = EtlSettings()
    factory = SourceApiClientResourceFactory(settings)
    return factory.get_client()


@resource
def target_db_engine_resource(_) -> TargetDatabaseEngineManager:
    settings = TargetDatabaseSettings()
    factory = TargetDatabaseEngineResourceFactory(settings)
    return factory.get_engine_manager()

