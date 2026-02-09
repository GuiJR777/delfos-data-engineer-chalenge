# Tests for EtlRunner.

from datetime import date, datetime
from unittest.mock import MagicMock

from etl.constants import SOURCE_SIGNAL_NAMES
from etl.date_range import DateRange
from etl.entities import AggregatedSignalPoint
from etl.run import EtlRunner


class TestDoRun:
    def test_when_called_should_execute_pipeline(self):
        # Arrange

        api_client = MagicMock()
        api_client.do_fetch_data.return_value = [
            {"timestamp": "2024-01-01T00:00:00"}
        ]

        date_range = DateRange(
            start=datetime(2024, 1, 1, 0, 0, 0),
            end=datetime(2024, 1, 2, 0, 0, 0),
        )
        date_range_calculator = MagicMock()
        date_range_calculator.get_date_range.return_value = date_range

        aggregated_points = [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.0,
            )
        ]
        aggregator = MagicMock()
        aggregator.do_aggregate.return_value = aggregated_points

        loader = MagicMock()
        loader.do_load.return_value = 1

        bootstrapper = MagicMock()
        engine_manager = MagicMock()

        runner = EtlRunner(
            api_client=api_client,
            date_range_calculator=date_range_calculator,
            aggregator=aggregator,
            loader=loader,
            bootstrapper=bootstrapper,
            engine_manager=engine_manager,
        )

        # Act

        result = runner.do_run(date(2024, 1, 1))

        # Assert

        assert result == 1
        engine_manager.do_startup.assert_called_once_with()
        bootstrapper.do_bootstrap.assert_called_once_with()
        api_client.do_fetch_data.assert_called_once_with(
            start_timestamp="2024-01-01T00:00:00",
            end_timestamp="2024-01-02T00:00:00",
            signal_names=SOURCE_SIGNAL_NAMES,
        )
        aggregator.do_aggregate.assert_called_once_with(
            data_rows=api_client.do_fetch_data.return_value,
            signal_names=SOURCE_SIGNAL_NAMES,
        )
        loader.do_load.assert_called_once()
        api_client.do_close.assert_called_once_with()
        engine_manager.do_shutdown.assert_called_once_with()

