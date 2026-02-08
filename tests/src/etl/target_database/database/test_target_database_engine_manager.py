# Tests for TargetDatabaseEngineManager.

from unittest.mock import MagicMock

import pytest

import etl.target_database.database as database_module
from etl.target_database.database import (
    ENGINE_NOT_INITIALIZED_MESSAGE,
    TargetDatabaseEngineManager,
)


class TestDoStartup:
    def test_when_called_should_initialize_engine(self, monkeypatch):
        # Arrange

        database_url = "postgresql://user@host/target"
        engine = MagicMock()

        settings = MagicMock()
        settings.get_target_database_url.return_value = database_url

        create_engine = MagicMock(return_value=engine)
        monkeypatch.setattr(database_module, "create_engine", create_engine)

        manager = TargetDatabaseEngineManager(settings)

        # Act

        manager.do_startup()

        # Assert

        create_engine.assert_called_once_with(database_url)
        assert manager.get_database_engine() == engine


class TestDoShutdown:
    def test_when_engine_is_initialized_should_dispose_and_reset(self):
        # Arrange

        engine = MagicMock()
        settings = MagicMock()

        manager = TargetDatabaseEngineManager(settings)
        manager._database_engine = engine

        # Act

        manager.do_shutdown()

        # Assert

        engine.dispose.assert_called_once_with()
        assert manager.is_database_engine_initialized() is False

    def test_when_engine_is_not_initialized_should_do_nothing(self):
        # Arrange

        settings = MagicMock()
        manager = TargetDatabaseEngineManager(settings)

        # Act

        manager.do_shutdown()

        # Assert

        assert manager.is_database_engine_initialized() is False


class TestIsDatabaseEngineInitialized:
    def test_when_engine_is_missing_should_return_false(self):
        # Arrange

        settings = MagicMock()
        manager = TargetDatabaseEngineManager(settings)

        # Act

        result = manager.is_database_engine_initialized()

        # Assert

        assert result is False

    def test_when_engine_is_available_should_return_true(self):
        # Arrange

        settings = MagicMock()
        manager = TargetDatabaseEngineManager(settings)
        manager._database_engine = MagicMock()

        # Act

        result = manager.is_database_engine_initialized()

        # Assert

        assert result is True


class TestGetDatabaseEngine:
    def test_when_engine_is_missing_should_raise_error(self):
        # Arrange

        settings = MagicMock()
        manager = TargetDatabaseEngineManager(settings)

        # Act

        with pytest.raises(RuntimeError) as error:
            manager.get_database_engine()

        # Assert
        assert str(error.value) == ENGINE_NOT_INITIALIZED_MESSAGE

    def test_when_engine_is_initialized_should_return_engine(self):
        # Arrange

        engine = MagicMock()
        settings = MagicMock()

        manager = TargetDatabaseEngineManager(settings)
        manager._database_engine = engine

        # Act

        result = manager.get_database_engine()

        # Assert

        assert result == engine
