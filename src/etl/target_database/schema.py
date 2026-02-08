# Criacao do schema do banco alvo.

from etl.target_database.database import TargetDatabaseEngineManager
from etl.target_database.models import Base


class TargetDatabaseSchemaManager:
    def __init__(
        self,
        engine_manager: TargetDatabaseEngineManager,
    ) -> None:
        self._engine_manager = engine_manager

    def do_create_schema(self) -> None:
        database_engine = self._engine_manager.get_database_engine()
        Base.metadata.create_all(database_engine)

