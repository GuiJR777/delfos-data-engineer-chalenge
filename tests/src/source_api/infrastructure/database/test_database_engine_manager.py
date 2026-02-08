# Tests for DatabaseEngineManager.

from unittest.mock import MagicMock

import pytest

import source_api.infrastructure.database as database_module


class TestInit:
    def test_when_instance_is_created_should_be_not_initialized(self):
        # Arrange

        settings = MagicMock()

        # Act

        manager = database_module.DatabaseEngineManager(settings)

        # Assert

        assert manager.is_database_engine_initialized() is False


class TestIsDatabaseEngineInitialized:
    def test_when_engine_is_missing_should_return_false(self):
        # Arrange

        settings = MagicMock()
        manager = database_module.DatabaseEngineManager(settings)

        # Act

        result = manager.is_database_engine_initialized()

        # Assert

        assert result is False

    def test_when_engine_is_set_should_return_true(self):
        # Arrange

        settings = MagicMock()
        manager = database_module.DatabaseEngineManager(settings)
        manager._database_engine = MagicMock()

        # Act

        result = manager.is_database_engine_initialized()

        # Assert

        assert result is True


class TestDoStartup:
    def test_when_called_should_create_engine(self, monkeypatch):
        # Arrange

        settings = MagicMock()
        settings.get_source_database_url.return_value = "db_url"
        engine = MagicMock()
        create_engine = MagicMock(return_value=engine)
        monkeypatch.setattr(database_module, "create_engine", create_engine)
        manager = database_module.DatabaseEngineManager(settings)

        # Act

        manager.do_startup()

        # Assert

        create_engine.assert_called_once_with("db_url")
        assert manager.is_database_engine_initialized() is True
        assert manager.get_database_engine() == engine


class TestDoShutdown:
    def test_when_called_should_dispose_engine(self):
        # Arrange

        settings = MagicMock()
        manager = database_module.DatabaseEngineManager(settings)
        engine = MagicMock()
        manager._database_engine = engine

        # Act

        manager.do_shutdown()

        # Assert

        engine.dispose.assert_called_once_with()
        assert manager.is_database_engine_initialized() is False


class TestGetDatabaseEngine:
    def test_when_engine_is_missing_should_raise_error(self):
        # Arrange

        settings = MagicMock()
        manager = database_module.DatabaseEngineManager(settings)

        # Act

        with pytest.raises(RuntimeError) as excinfo:
            manager.get_database_engine()

        # Assert

        assert str(excinfo.value) == database_module.ENGINE_NOT_INITIALIZED_MESSAGE

    def test_when_engine_is_set_should_return_engine(self):
        # Arrange

        settings = MagicMock()
        manager = database_module.DatabaseEngineManager(settings)
        engine = MagicMock()
        manager._database_engine = engine

        # Act

        result = manager.get_database_engine()

        # Assert

        assert result == engine

