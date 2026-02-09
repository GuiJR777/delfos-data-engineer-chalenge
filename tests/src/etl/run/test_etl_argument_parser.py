# Tests for EtlArgumentParser.

from datetime import date
import sys

import pytest

from etl.run import EtlArgumentParser


class TestGetTargetDate:
    def test_when_date_argument_is_provided_should_parse(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(
            sys,
            "argv",
            ["etl.run", "--date", "2024-01-01"],
        )
        parser = EtlArgumentParser()

        # Act

        result = parser.get_target_date()

        # Assert

        assert result == date(2024, 1, 1)


class TestParseDate:
    def test_when_date_is_invalid_should_raise_error(self):
        # Arrange

        parser = EtlArgumentParser()

        # Act

        with pytest.raises(ValueError):
            parser._parse_date("invalid-date")

        # Assert

