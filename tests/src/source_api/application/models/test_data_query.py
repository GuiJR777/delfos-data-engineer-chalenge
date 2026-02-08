# Tests for DataQuery.

from datetime import datetime

from source_api.application.models import DataQuery


class TestInit:
    def test_when_data_query_is_created_should_set_attributes(self):
        # Arrange

        start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        end_timestamp = datetime(2024, 1, 1, 1, 0, 0)
        signal_names = ["wind_speed", "power"]
        limit = 100
        offset = 10

        # Act

        data_query = DataQuery(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            signal_names=signal_names,
            limit=limit,
            offset=offset,
        )

        # Assert

        assert data_query.start_timestamp == start_timestamp
        assert data_query.end_timestamp == end_timestamp
        assert data_query.signal_names == signal_names
        assert data_query.limit == limit
        assert data_query.offset == offset

