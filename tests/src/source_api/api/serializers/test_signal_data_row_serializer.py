# Tests for SignalDataRowSerializer.

from datetime import datetime
from unittest.mock import MagicMock

from source_api.api.serializers import SignalDataRowSerializer


class TestGetPayload:
    def test_when_data_row_is_provided_should_return_payload(self):
        # Arrange

        timestamp = datetime(2024, 1, 1, 0, 0, 0)
        data_row = MagicMock()
        data_row.timestamp = timestamp
        data_row.signal_values = {"wind_speed": 1.0, "power": 2.0}
        serializer = SignalDataRowSerializer()
        signal_names = ["wind_speed", "power"]
        expected = {
            "timestamp": timestamp,
            "wind_speed": 1.0,
            "power": 2.0,
        }

        # Act

        result = serializer.get_payload(data_row, signal_names)

        # Assert

        assert result == expected


class TestGetPayloads:
    def test_when_multiple_rows_are_provided_should_return_payloads(self):
        # Arrange

        timestamp_one = datetime(2024, 1, 1, 0, 0, 0)
        timestamp_two = datetime(2024, 1, 1, 0, 1, 0)
        row_one = MagicMock()
        row_one.timestamp = timestamp_one
        row_one.signal_values = {"wind_speed": 1.0, "power": 2.0}
        row_two = MagicMock()
        row_two.timestamp = timestamp_two
        row_two.signal_values = {"wind_speed": 1.1, "power": 2.1}
        serializer = SignalDataRowSerializer()
        signal_names = ["wind_speed", "power"]
        expected = [
            {
                "timestamp": timestamp_one,
                "wind_speed": 1.0,
                "power": 2.0,
            },
            {
                "timestamp": timestamp_two,
                "wind_speed": 1.1,
                "power": 2.1,
            },
        ]

        # Act

        result = serializer.get_payloads([row_one, row_two], signal_names)

        # Assert

        assert result == expected

