# Ciclo de vida da aplicacao da API.

from source_api.infrastructure.database import DatabaseEngineManager


class ApplicationLifecycle:
    def __init__(self, database_engine_manager: DatabaseEngineManager) -> None:
        self._database_engine_manager = database_engine_manager

    def do_startup(self) -> None:
        self._database_engine_manager.do_startup()

    def do_shutdown(self) -> None:
        self._database_engine_manager.do_shutdown()

