# Tests for DateRange.

from datetime import datetime

from etl.date_range import DateRange


class TestInit:
    def test_when_created_should_set_attributes(self):
        # Arrange

        start = datetime(2024, 1, 1, 0, 0, 0)
        end = datetime(2024, 1, 2, 0, 0, 0)

        # Act

        date_range = DateRange(start=start, end=end)

        # Assert

        assert date_range.start == start
        assert date_range.end == end

