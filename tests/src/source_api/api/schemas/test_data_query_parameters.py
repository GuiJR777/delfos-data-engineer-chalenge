# Tests for DataQueryParameters.

from datetime import datetime

from source_api.api.schemas import DataQueryParameters


class TestInit:
    def test_when_parameters_are_provided_should_set_attributes(self):
        # Arrange

        start = datetime(2024, 1, 1, 0, 0, 0)
        end = datetime(2024, 1, 1, 1, 0, 0)
        signals = ["wind_speed", "power"]
        limit = 100
        offset = 10

        # Act

        parameters = DataQueryParameters(
            start=start,
            end=end,
            signals=signals,
            limit=limit,
            offset=offset,
        )

        # Assert

        assert parameters.start_timestamp == start
        assert parameters.end_timestamp == end
        assert parameters.signal_names == signals
        assert parameters.limit == limit
        assert parameters.offset == offset

