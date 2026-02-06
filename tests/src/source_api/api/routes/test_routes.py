# Tests for API routes.

from datetime import datetime
from unittest.mock import MagicMock

import source_api.api.routes as routes_module


class TestGetHealth:
    def test_when_called_should_return_status_ok(self):
        # Arrange

        # Act

        result = routes_module.get_health()

        # Assert

        assert result == {"status": "ok"}


class TestGetData:
    def test_when_called_should_return_serialized_payloads(self, monkeypatch):
        # Arrange

        parameters = MagicMock()
        parameters.start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        parameters.end_timestamp = datetime(2024, 1, 1, 1, 0, 0)
        parameters.signal_names = ["wind_speed"]
        parameters.limit = 10
        parameters.offset = 0

        signal_name_parser = MagicMock()
        normalized_signal_names = ["wind_speed"]
        signal_name_parser.get_normalized_signal_names.return_value = (
            normalized_signal_names
        )

        use_case = MagicMock()
        data_rows = ["row"]
        use_case.get_data_rows.return_value = data_rows

        serializer = MagicMock()
        payloads = [{"timestamp": "2024-01-01T00:00:00"}]
        serializer.get_payloads.return_value = payloads

        data_query = MagicMock()
        data_query_class = MagicMock(return_value=data_query)
        monkeypatch.setattr(routes_module, "DataQuery", data_query_class)

        # Act

        result = routes_module.get_data(
            parameters,
            signal_name_parser,
            serializer,
            use_case,
        )

        # Assert

        data_query_class.assert_called_once_with(
            start_timestamp=parameters.start_timestamp,
            end_timestamp=parameters.end_timestamp,
            signal_names=normalized_signal_names,
            limit=parameters.limit,
            offset=parameters.offset,
        )
        use_case.get_data_rows.assert_called_once_with(data_query)
        serializer.get_payloads.assert_called_once_with(
            data_rows,
            normalized_signal_names,
        )
        assert result == payloads

