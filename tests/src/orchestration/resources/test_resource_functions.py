# Tests for resource functions.

from unittest.mock import MagicMock

import orchestration.resources as resources_module


class TestSourceApiClientResource:
    def test_when_called_should_return_client(self, monkeypatch):
        # Arrange

        settings = MagicMock()
        settings_class = MagicMock(return_value=settings)
        monkeypatch.setattr(
            resources_module,
            "EtlSettings",
            settings_class,
        )

        factory = MagicMock()
        factory.get_client.return_value = MagicMock()
        factory_class = MagicMock(return_value=factory)
        monkeypatch.setattr(
            resources_module,
            "SourceApiClientResourceFactory",
            factory_class,
        )

        # Act

        resource_definition = resources_module.source_api_client_resource
        result = resource_definition.resource_fn(None)

        # Assert

        assert result == factory.get_client.return_value
        settings_class.assert_called_once_with()
        factory_class.assert_called_once_with(settings)
        factory.get_client.assert_called_once_with()


class TestTargetDbEngineResource:
    def test_when_called_should_return_engine_manager(self, monkeypatch):
        # Arrange

        settings = MagicMock()
        settings_class = MagicMock(return_value=settings)
        monkeypatch.setattr(
            resources_module,
            "TargetDatabaseSettings",
            settings_class,
        )

        factory = MagicMock()
        factory.get_engine_manager.return_value = MagicMock()
        factory_class = MagicMock(return_value=factory)
        monkeypatch.setattr(
            resources_module,
            "TargetDatabaseEngineResourceFactory",
            factory_class,
        )

        # Act

        resource_definition = resources_module.target_db_engine_resource
        result = resource_definition.resource_fn(None)

        # Assert

        assert result == factory.get_engine_manager.return_value
        settings_class.assert_called_once_with()
        factory_class.assert_called_once_with(settings)
        factory.get_engine_manager.assert_called_once_with()

