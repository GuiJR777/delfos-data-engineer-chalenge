# Tests for EtlRunnerFactory.

from unittest.mock import MagicMock

import etl.run as run_module
from etl.run import EtlRunnerFactory


class TestGetRunner:
    def test_when_dependencies_are_missing_should_build_defaults(
        self,
        monkeypatch,
    ):
        # Arrange

        settings = MagicMock()
        settings.get_api_base_url.return_value = "http://api"
        settings.get_api_timeout_seconds.return_value = 1.0
        settings.get_api_retry_attempts.return_value = 2
        settings.get_api_limit.return_value = 10
        settings.get_api_offset.return_value = 0

        target_settings = MagicMock()
        target_settings_class = MagicMock(return_value=target_settings)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseSettings",
            target_settings_class,
        )

        engine_manager = MagicMock()
        engine_manager_class = MagicMock(return_value=engine_manager)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseEngineManager",
            engine_manager_class,
        )

        session_factory = MagicMock()
        session_factory_class = MagicMock(return_value=session_factory)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseSessionFactory",
            session_factory_class,
        )

        schema_manager = MagicMock()
        schema_manager_class = MagicMock(return_value=schema_manager)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseSchemaManager",
            schema_manager_class,
        )

        signal_seeder = MagicMock()
        signal_seeder_class = MagicMock(return_value=signal_seeder)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseSignalSeeder",
            signal_seeder_class,
        )

        bootstrapper = MagicMock()
        bootstrapper_class = MagicMock(return_value=bootstrapper)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseBootstrapper",
            bootstrapper_class,
        )

        api_client = MagicMock()
        api_client_class = MagicMock(return_value=api_client)
        monkeypatch.setattr(
            run_module,
            "SourceApiClient",
            api_client_class,
        )

        aggregator = MagicMock()
        aggregator_class = MagicMock(return_value=aggregator)
        monkeypatch.setattr(
            run_module,
            "TenMinuteAggregator",
            aggregator_class,
        )

        loader = MagicMock()
        loader_class = MagicMock(return_value=loader)
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseLoader",
            loader_class,
        )

        calculator = MagicMock()
        calculator_class = MagicMock(return_value=calculator)
        monkeypatch.setattr(
            run_module,
            "EtlDateRangeCalculator",
            calculator_class,
        )

        factory = EtlRunnerFactory(settings)

        # Act

        result = factory.get_runner()

        # Assert

        assert result is not None
        target_settings_class.assert_called_once_with()
        engine_manager_class.assert_called_once_with(target_settings)
        api_client_class.assert_called_once_with(
            base_url="http://api",
            timeout_seconds=1.0,
            retry_attempts=2,
            api_limit=10,
            api_offset=0,
        )

    def test_when_dependencies_are_provided_should_reuse_them(
        self,
        monkeypatch,
    ):
        # Arrange

        settings = MagicMock()
        api_client = MagicMock()
        engine_manager = MagicMock()

        target_settings_class = MagicMock()
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseSettings",
            target_settings_class,
        )

        engine_manager_class = MagicMock()
        monkeypatch.setattr(
            run_module,
            "TargetDatabaseEngineManager",
            engine_manager_class,
        )

        api_client_class = MagicMock()
        monkeypatch.setattr(
            run_module,
            "SourceApiClient",
            api_client_class,
        )

        factory = EtlRunnerFactory(settings)

        # Act

        result = factory.get_runner(
            api_client=api_client,
            engine_manager=engine_manager,
        )

        # Assert

        assert result is not None
        target_settings_class.assert_not_called()
        engine_manager_class.assert_not_called()
        api_client_class.assert_not_called()

