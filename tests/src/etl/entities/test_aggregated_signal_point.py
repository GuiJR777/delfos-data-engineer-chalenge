# Tests for AggregatedSignalPoint.

from datetime import datetime

from etl.entities import AggregatedSignalPoint


class TestInit:
    def test_when_created_should_set_attributes(self):
        # Arrange

        timestamp = datetime(2024, 1, 1, 0, 0, 0)
        signal_name = "wind_speed_mean"
        value = 1.23

        # Act

        point = AggregatedSignalPoint(
            timestamp=timestamp,
            signal_name=signal_name,
            value=value,
        )

        # Assert

        assert point.timestamp == timestamp
        assert point.signal_name == signal_name
        assert point.value == value

