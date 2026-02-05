import pytest

from scripts import seed_source_db


class TestNormalizePgUrl:
    @pytest.mark.parametrize(
        "input_url, expected",
        [
            (
                "postgresql+psycopg2://user:pass@host:5432/db",
                "postgresql://user:pass@host:5432/db",
            ),
            (
                "postgresql://user:pass@host:5432/db",
                "postgresql://user:pass@host:5432/db",
            ),
        ],
    )
    def test_when_url_is_provided_should_return_expected_normalized_url(self, input_url, expected):
        # Arrange

        # Act

        result = seed_source_db.normalize_pg_url(input_url)

        # Assert

        assert result == expected
