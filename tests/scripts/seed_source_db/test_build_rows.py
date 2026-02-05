from datetime import datetime, timedelta

import pytest

from scripts import seed_source_db


class TestBuildRows:
    @pytest.mark.parametrize(
        "minutes",
        [1, 3, 10],
    )
    def test_when_interval_has_minutes_should_generate_expected_rows(self, minutes):
        # Arrange

        start_ts = datetime(2024, 1, 1, 0, 0, 0)
        end_ts = start_ts + timedelta(minutes=minutes)
        expected_count = minutes
        expected_last_ts = start_ts + timedelta(minutes=expected_count - 1)

        # Act

        rows = seed_source_db.build_rows(start_ts, end_ts, seed=1)

        # Assert

        assert len(rows) == expected_count
        assert rows[0][0] == start_ts
        assert rows[-1][0] == expected_last_ts
        assert rows[0][1] >= 0.0
        assert rows[0][2] >= 0.0

    def test_when_start_equals_end_should_generate_zero_rows(self):
        # Arrange

        start_ts = datetime(2024, 1, 1, 0, 0, 0)
        end_ts = start_ts

        # Act

        rows = seed_source_db.build_rows(start_ts, end_ts, seed=1)

        # Assert

        assert rows == []
