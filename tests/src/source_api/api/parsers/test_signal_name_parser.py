# Tests for SignalNameParser.

import pytest

from source_api.api.parsers import SignalNameParser


class TestGetNormalizedSignalNames:
    @pytest.mark.parametrize(
        "signal_names, expected",
        [
            (["wind_speed", "power"], ["wind_speed", "power"]),
            (["wind_speed,power"], ["wind_speed", "power"]),
            ([" wind_speed ", " power "], ["wind_speed", "power"]),
            (["wind_speed", ""], ["wind_speed"]),
            ([], []),
        ],
    )
    def test_when_signal_names_are_provided_should_return_normalized_list(
        self,
        signal_names,
        expected,
    ):
        # Arrange

        parser = SignalNameParser()

        # Act

        result = parser.get_normalized_signal_names(signal_names)

        # Assert

        assert result == expected


class TestGetExpandedSignalNames:
    @pytest.mark.parametrize(
        "signal_names, expected",
        [
            (["wind_speed", "power"], ["wind_speed", "power"]),
            (["wind_speed,power"], ["wind_speed", "power"]),
            (
                ["wind_speed", "power,ambient_temperature"],
                ["wind_speed", "power", "ambient_temperature"],
            ),
        ],
    )
    def test_when_separator_is_present_should_expand_names(
        self,
        signal_names,
        expected,
    ):
        # Arrange

        parser = SignalNameParser()

        # Act

        result = parser._get_expanded_signal_names(signal_names)

        # Assert

        assert result == expected

