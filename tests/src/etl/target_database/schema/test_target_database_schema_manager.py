# Tests for TargetDatabaseSchemaManager.

from unittest.mock import MagicMock

import etl.target_database.schema as schema_module
from etl.target_database.schema import TargetDatabaseSchemaManager


class TestDoCreateSchema:
    def test_when_called_should_create_schema(self, monkeypatch):
        # Arrange

        engine = MagicMock()
        engine_manager = MagicMock()
        engine_manager.get_database_engine.return_value = engine

        create_all = MagicMock()
        monkeypatch.setattr(
            schema_module.Base.metadata,
            "create_all",
            create_all,
        )

        manager = TargetDatabaseSchemaManager(engine_manager)

        # Act

        manager.do_create_schema()

        # Assert

        create_all.assert_called_once_with(engine)

