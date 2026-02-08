# Tests for TargetDatabaseSessionFactory.

from unittest.mock import MagicMock

import etl.target_database.database as database_module
from etl.target_database.database import TargetDatabaseSessionFactory


class TestGetSession:
    def test_when_called_should_return_session(self, monkeypatch):
        # Arrange

        engine = MagicMock()
        session = MagicMock()
        session_factory_instance = MagicMock(return_value=session)

        engine_manager = MagicMock()
        engine_manager.get_database_engine.return_value = engine

        sessionmaker_mock = MagicMock(
            return_value=session_factory_instance,
        )
        monkeypatch.setattr(database_module, "sessionmaker", sessionmaker_mock)

        factory = TargetDatabaseSessionFactory(engine_manager)

        # Act

        result = factory.get_session()

        # Assert

        sessionmaker_mock.assert_called_once_with(
            bind=engine,
            expire_on_commit=False,
        )
        assert result == session

