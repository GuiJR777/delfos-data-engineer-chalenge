# Tests for API constants.

from source_api.api import constants


class TestConstants:
    def test_when_constants_are_loaded_should_match_expected_values(self):
        # Arrange

        # Act

        # Assert
        assert constants.SIGNAL_SEPARATOR == ","
        assert constants.DEFAULT_LIMIT == 10_000
        assert constants.MAX_LIMIT == 50_000
        assert constants.MIN_LIMIT == 1
        assert constants.DEFAULT_OFFSET == 0
        assert constants.ZERO_COUNT == 0

