# Tests for SqlAlchemySourceDataRepository.

from datetime import datetime
from unittest.mock import MagicMock, call

import source_api.infrastructure.repository as repository_module


class TestInit:
    def test_when_instance_is_created_should_store_engine(self):
        # Arrange

        engine = MagicMock()

        # Act

        repository = repository_module.SqlAlchemySourceDataRepository(engine)

        # Assert

        assert repository._database_engine == engine


class TestBuildSignalDataRow:
    def test_when_row_is_provided_should_build_entity(self, monkeypatch):
        # Arrange

        engine = MagicMock()
        repository = repository_module.SqlAlchemySourceDataRepository(engine)
        signal_data_row = MagicMock()
        signal_data_row_class = MagicMock(return_value=signal_data_row)
        monkeypatch.setattr(
            repository_module,
            "SignalDataRow",
            signal_data_row_class,
        )
        row = {
            "timestamp": datetime(2024, 1, 1, 0, 0, 0),
            "wind_speed": 1.0,
        }
        signal_names = ["wind_speed"]

        # Act

        result = repository._build_signal_data_row(row, signal_names)

        # Assert

        signal_data_row_class.assert_called_once_with(
            timestamp=row["timestamp"],
            signal_values={"wind_speed": 1.0},
        )
        assert result == signal_data_row


class TestGetDataRows:
    def test_when_rows_are_found_should_return_entities(self, monkeypatch):
        # Arrange

        engine = MagicMock()
        connection = MagicMock()
        result_proxy = MagicMock()
        row_one = {
            "timestamp": datetime(2024, 1, 1, 0, 0, 0),
            "wind_speed": 1.0,
            "power": 2.0,
        }
        row_two = {
            "timestamp": datetime(2024, 1, 1, 0, 1, 0),
            "wind_speed": 1.1,
            "power": 2.1,
        }
        result_proxy.mappings.return_value.all.return_value = [row_one, row_two]
        connection.execute.return_value = result_proxy
        connection_context = MagicMock()
        connection_context.__enter__.return_value = connection
        engine.connect.return_value = connection_context

        query = MagicMock()
        query_text = MagicMock(return_value=query)
        monkeypatch.setattr(repository_module, "text", query_text)

        repository = repository_module.SqlAlchemySourceDataRepository(engine)
        repository._build_signal_data_row = MagicMock(
            side_effect=["row1", "row2"]
        )

        start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        end_timestamp = datetime(2024, 1, 1, 1, 0, 0)
        signal_names = ["wind_speed", "power"]

        expected_query = (
            "SELECT timestamp, wind_speed, power "
            "FROM data "
            "WHERE timestamp >= :start_timestamp "
            "AND timestamp < :end_timestamp "
            "ORDER BY timestamp ASC "
            "LIMIT :limit OFFSET :offset"
        )

        # Act

        result = repository.get_data_rows(
            start_timestamp,
            end_timestamp,
            signal_names,
            10,
            0,
        )

        # Assert

        query_text.assert_called_once_with(expected_query)
        connection.execute.assert_called_once_with(
            query,
            {
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "limit": 10,
                "offset": 0,
            },
        )
        repository._build_signal_data_row.assert_has_calls(
            [
                call(row_one, signal_names),
                call(row_two, signal_names),
            ]
        )
        assert result == ["row1", "row2"]

