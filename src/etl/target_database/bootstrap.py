# Orquestracao da inicializacao do banco alvo.

from etl.target_database.schema import TargetDatabaseSchemaManager
from etl.target_database.seed import TargetDatabaseSignalSeeder


class TargetDatabaseBootstrapper:
    def __init__(
        self,
        schema_manager: TargetDatabaseSchemaManager,
        signal_seeder: TargetDatabaseSignalSeeder,
    ) -> None:
        self._schema_manager = schema_manager
        self._signal_seeder = signal_seeder

    def do_bootstrap(self) -> None:
        self._schema_manager.do_create_schema()
        self._signal_seeder.do_seed_signals()

