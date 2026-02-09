# Tests for TenMinuteAggregator.

from datetime import datetime

import pandas

from etl.aggregator import TenMinuteAggregator
from etl.entities import AggregatedSignalPoint


class TestDoAggregate:
    def test_when_no_rows_should_return_empty_list(self):
        # Arrange

        aggregator = TenMinuteAggregator()

        # Act

        result = aggregator.do_aggregate(
            data_rows=[],
            signal_names=("wind_speed", "power"),
        )

        # Assert

        assert result == []

    def test_when_rows_are_present_should_return_aggregated_points(
        self,
    ):
        # Arrange

        data_rows = [
            {
                "timestamp": "2024-01-01T00:00:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:01:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:02:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:03:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:04:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:05:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:06:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:07:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:08:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": "2024-01-01T00:09:00",
                "wind_speed": 1.0,
                "power": 2.0,
            },
        ]
        aggregator = TenMinuteAggregator()
        expected_timestamp = datetime(2024, 1, 1, 0, 0, 0)

        # Act

        result = aggregator.do_aggregate(
            data_rows=data_rows,
            signal_names=("wind_speed", "power"),
        )

        # Assert

        assert len(result) == 8
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="wind_speed_mean",
            value=1.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="wind_speed_min",
            value=1.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="wind_speed_max",
            value=1.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="wind_speed_std",
            value=0.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="power_mean",
            value=2.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="power_min",
            value=2.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="power_max",
            value=2.0,
        ) in result
        assert AggregatedSignalPoint(
            timestamp=expected_timestamp,
            signal_name="power_std",
            value=0.0,
        ) in result


class TestGetFlatColumns:
    def test_when_multi_index_is_provided_should_flatten(self):
        # Arrange

        aggregator = TenMinuteAggregator()
        multi_index = pandas.MultiIndex.from_tuples(
            [("wind_speed", "mean"), ("power", "max")]
        )

        # Act

        result = aggregator._get_flat_columns(multi_index)

        # Assert

        assert result == ["wind_speed_mean", "power_max"]


class TestGetAggregatedPoints:
    def test_when_rows_are_provided_should_return_points(self):
        # Arrange

        aggregator = TenMinuteAggregator()
        data_frame = pandas.DataFrame(
            [
                {
                    "timestamp": datetime(2024, 1, 1, 0, 0, 0),
                    "signal_name": "wind_speed_mean",
                    "value": 1.5,
                },
                {
                    "timestamp": datetime(2024, 1, 1, 0, 10, 0),
                    "signal_name": "power_mean",
                    "value": 2.5,
                },
            ]
        )

        # Act

        result = aggregator._get_aggregated_points(data_frame)

        # Assert

        assert result == [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.5,
            ),
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 10, 0),
                signal_name="power_mean",
                value=2.5,
            ),
        ]


class TestNormalizeTimestamp:
    def test_when_datetime_is_provided_should_return_same_value(
        self,
    ):
        # Arrange

        aggregator = TenMinuteAggregator()
        timestamp_value = datetime(2024, 1, 1, 0, 0, 0)

        # Act

        result = aggregator._normalize_timestamp(timestamp_value)

        # Assert

        assert result == timestamp_value

    def test_when_string_is_provided_should_parse_timestamp(self):
        # Arrange

        aggregator = TenMinuteAggregator()
        timestamp_value = "2024-01-01T00:00:00"

        # Act

        result = aggregator._normalize_timestamp(timestamp_value)

        # Assert

        assert result == datetime(2024, 1, 1, 0, 0, 0)

