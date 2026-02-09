# Tests for run_daily_etl.

from datetime import date
from unittest.mock import MagicMock

import etl.run as run_module
from etl.run import run_daily_etl


class TestRunDailyEtl:
    def test_when_called_should_run_with_factory(self, monkeypatch):
        # Arrange

        runner = MagicMock()
        runner.do_run.return_value = 3

        factory = MagicMock()
        factory.get_runner.return_value = runner

        factory_class = MagicMock(return_value=factory)
        monkeypatch.setattr(run_module, "EtlRunnerFactory", factory_class)

        settings = MagicMock()
        api_client = MagicMock()
        engine_manager = MagicMock()

        # Act

        result = run_daily_etl(
            target_date=date(2024, 1, 1),
            api_client=api_client,
            engine_manager=engine_manager,
            settings=settings,
        )

        # Assert

        assert result == 3
        factory_class.assert_called_once_with(settings)
        factory.get_runner.assert_called_once_with(
            api_client=api_client,
            engine_manager=engine_manager,
        )
        runner.do_run.assert_called_once_with(date(2024, 1, 1))

