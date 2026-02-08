# Tests for DependencyProvider.

from unittest.mock import MagicMock

import pytest
from fastapi import status

import source_api.api.dependencies as dependencies_module


class TestInit:
    def test_when_instance_is_created_should_store_manager(self):
        # Arrange

        manager = MagicMock()

        # Act

        provider = dependencies_module.DependencyProvider(manager)

        # Assert

        assert provider._database_engine_manager == manager


class TestGetSignalNameParser:
    def test_when_called_should_return_parser_instance(self, monkeypatch):
        # Arrange

        manager = MagicMock()
        provider = dependencies_module.DependencyProvider(manager)
        parser_instance = MagicMock()
        parser_class = MagicMock(return_value=parser_instance)
        monkeypatch.setattr(
            dependencies_module,
            "SignalNameParser",
            parser_class,
        )

        # Act

        result = provider.get_signal_name_parser()

        # Assert

        parser_class.assert_called_once_with()
        assert result == parser_instance


class TestGetSignalDataRowSerializer:
    def test_when_called_should_return_serializer_instance(self, monkeypatch):
        # Arrange

        manager = MagicMock()
        provider = dependencies_module.DependencyProvider(manager)
        serializer_instance = MagicMock()
        serializer_class = MagicMock(return_value=serializer_instance)
        monkeypatch.setattr(
            dependencies_module,
            "SignalDataRowSerializer",
            serializer_class,
        )

        # Act

        result = provider.get_signal_data_row_serializer()

        # Assert

        serializer_class.assert_called_once_with()
        assert result == serializer_instance


class TestGetDataQueryValidator:
    def test_when_called_should_return_validator_instance(self, monkeypatch):
        # Arrange

        manager = MagicMock()
        provider = dependencies_module.DependencyProvider(manager)
        validator_instance = MagicMock()
        validator_class = MagicMock(return_value=validator_instance)
        allowed_signals = ("wind_speed", "power")
        monkeypatch.setattr(
            dependencies_module,
            "DataQueryValidator",
            validator_class,
        )
        monkeypatch.setattr(
            dependencies_module,
            "ALLOWED_SIGNAL_NAMES",
            allowed_signals,
        )

        # Act

        result = provider.get_data_query_validator()

        # Assert

        validator_class.assert_called_once_with(allowed_signals)
        assert result == validator_instance


class TestGetRepository:
    def test_when_engine_is_initialized_should_return_repository(
        self,
        monkeypatch,
    ):
        # Arrange

        manager = MagicMock()
        manager.is_database_engine_initialized.return_value = True
        database_engine = MagicMock()
        manager.get_database_engine.return_value = database_engine
        repository_instance = MagicMock()
        repository_class = MagicMock(return_value=repository_instance)
        monkeypatch.setattr(
            dependencies_module,
            "SqlAlchemySourceDataRepository",
            repository_class,
        )
        provider = dependencies_module.DependencyProvider(manager)

        # Act

        result = provider.get_repository()

        # Assert

        repository_class.assert_called_once_with(database_engine)
        assert result == repository_instance

    def test_when_engine_is_not_initialized_should_raise_http_exception(
        self,
    ):
        # Arrange

        manager = MagicMock()
        manager.is_database_engine_initialized.return_value = False
        provider = dependencies_module.DependencyProvider(manager)

        # Act

        with pytest.raises(Exception) as excinfo:
            provider.get_repository()

        # Assert

        assert excinfo.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


class TestGetUseCase:
    def test_when_called_should_return_use_case_instance(self, monkeypatch):
        # Arrange

        manager = MagicMock()
        provider = dependencies_module.DependencyProvider(manager)
        repository = MagicMock()
        validator = MagicMock()
        provider.get_repository = MagicMock(return_value=repository)
        provider.get_data_query_validator = MagicMock(return_value=validator)
        use_case_instance = MagicMock()
        use_case_class = MagicMock(return_value=use_case_instance)
        monkeypatch.setattr(
            dependencies_module,
            "GetDataUseCase",
            use_case_class,
        )

        # Act

        result = provider.get_use_case()

        # Assert

        use_case_class.assert_called_once_with(repository, validator)
        assert result == use_case_instance

