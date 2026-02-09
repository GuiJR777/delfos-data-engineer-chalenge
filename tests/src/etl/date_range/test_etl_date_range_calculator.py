# Tests for EtlDateRangeCalculator.

from datetime import date, datetime

from etl.date_range import EtlDateRangeCalculator


class TestGetDateRange:
    def test_when_date_is_provided_should_return_start_and_end(self):
        # Arrange

        target_date = date(2024, 1, 1)
        calculator = EtlDateRangeCalculator()

        # Act

        result = calculator.get_date_range(target_date)

        # Assert

        assert result.start == datetime(2024, 1, 1, 0, 0, 0)
        assert result.end == datetime(2024, 1, 2, 0, 0, 0)

