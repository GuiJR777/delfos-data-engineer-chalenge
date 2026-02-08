# Tests for SignalDataRow.

from datetime import datetime

from source_api.domain.entities import SignalDataRow


class TestInit:
    def test_when_instance_is_created_should_set_attributes(self):
        # Arrange

        timestamp = datetime(2024, 1, 1, 0, 0, 0)
        signal_values = {"wind_speed": 1.0}

        # Act

        data_row = SignalDataRow(
            timestamp=timestamp,
            signal_values=signal_values,
        )

        # Assert

        assert data_row.timestamp == timestamp
        assert data_row.signal_values == signal_values

