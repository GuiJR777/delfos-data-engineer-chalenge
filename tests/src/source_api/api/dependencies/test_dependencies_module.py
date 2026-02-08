# Tests for dependency module functions.

from unittest.mock import MagicMock

import pytest

import source_api.api.dependencies as dependencies_module


class TestConfigureDependencies:
    def test_when_provider_is_configured_should_set_global(self, monkeypatch):
        # Arrange

        provider = MagicMock()
        monkeypatch.setattr(
            dependencies_module,
            "_dependency_provider",
            None,
        )

        # Act

        dependencies_module.configure_dependencies(provider)

        # Assert

        assert dependencies_module._dependency_provider == provider


class TestGetDependencyProvider:
    def test_when_provider_is_missing_should_raise_error(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(
            dependencies_module,
            "_dependency_provider",
            None,
        )

        # Act

        with pytest.raises(RuntimeError) as excinfo:
            dependencies_module._get_dependency_provider()

        # Assert

        assert (
            str(excinfo.value)
            == dependencies_module.DEPENDENCY_PROVIDER_NOT_CONFIGURED_MESSAGE
        )

    def test_when_provider_is_configured_should_return_provider(
        self,
        monkeypatch,
    ):
        # Arrange

        provider = MagicMock()
        monkeypatch.setattr(
            dependencies_module,
            "_dependency_provider",
            provider,
        )

        # Act

        result = dependencies_module._get_dependency_provider()

        # Assert

        assert result == provider


class TestGetSignalNameParser:
    def test_when_called_should_return_parser_instance(self, monkeypatch):
        # Arrange

        provider = MagicMock()
        parser_instance = MagicMock()
        provider.get_signal_name_parser.return_value = parser_instance
        monkeypatch.setattr(
            dependencies_module,
            "_dependency_provider",
            provider,
        )

        # Act

        result = dependencies_module.get_signal_name_parser()

        # Assert

        provider.get_signal_name_parser.assert_called_once_with()
        assert result == parser_instance


class TestGetSignalDataRowSerializer:
    def test_when_called_should_return_serializer_instance(self, monkeypatch):
        # Arrange

        provider = MagicMock()
        serializer_instance = MagicMock()
        provider.get_signal_data_row_serializer.return_value = serializer_instance
        monkeypatch.setattr(
            dependencies_module,
            "_dependency_provider",
            provider,
        )

        # Act

        result = dependencies_module.get_signal_data_row_serializer()

        # Assert

        provider.get_signal_data_row_serializer.assert_called_once_with()
        assert result == serializer_instance


class TestGetUseCase:
    def test_when_called_should_return_use_case_instance(self, monkeypatch):
        # Arrange

        provider = MagicMock()
        use_case_instance = MagicMock()
        provider.get_use_case.return_value = use_case_instance
        monkeypatch.setattr(
            dependencies_module,
            "_dependency_provider",
            provider,
        )

        # Act

        result = dependencies_module.get_use_case()

        # Assert

        provider.get_use_case.assert_called_once_with()
        assert result == use_case_instance

