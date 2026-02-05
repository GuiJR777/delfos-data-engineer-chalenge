# Gerenciamento do engine do banco de dados fonte.

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from source_api.infrastructure.settings import ApplicationSettings

ENGINE_NOT_INITIALIZED_MESSAGE: str = "Database engine is not initialized"


class DatabaseEngineManager:
    def __init__(self, settings: ApplicationSettings) -> None:
        self._settings = settings
        self._database_engine: Engine | None = None

    def do_startup(self) -> None:
        database_url = self._settings.get_source_database_url()
        self._database_engine = create_engine(database_url)

    def do_shutdown(self) -> None:
        has_database_engine = self._database_engine is not None
        if not has_database_engine:
            return

        self._database_engine.dispose()
        self._database_engine = None

    def is_database_engine_initialized(self) -> bool:
        return self._database_engine is not None

    def get_database_engine(self) -> Engine:
        has_database_engine = self._database_engine is not None
        if not has_database_engine:
            raise RuntimeError(ENGINE_NOT_INITIALIZED_MESSAGE)

        return self._database_engine

