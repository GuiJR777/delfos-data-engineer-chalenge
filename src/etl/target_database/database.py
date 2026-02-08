# Gerenciamento de engine e sessao do banco alvo.

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from etl.target_database.settings import TargetDatabaseSettings

ENGINE_NOT_INITIALIZED_MESSAGE: str = (
    "Target database engine is not initialized"
)


class TargetDatabaseEngineManager:
    def __init__(self, settings: TargetDatabaseSettings) -> None:
        self._settings = settings
        self._database_engine: Engine | None = None

    def do_startup(self) -> None:
        database_url = self._settings.get_target_database_url()
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


class TargetDatabaseSessionFactory:
    def __init__(
        self,
        engine_manager: TargetDatabaseEngineManager,
    ) -> None:
        self._engine_manager = engine_manager

    def get_session(self) -> Session:
        database_engine = self._engine_manager.get_database_engine()
        session_factory = sessionmaker(
            bind=database_engine,
            expire_on_commit=False,
        )
        return session_factory()

