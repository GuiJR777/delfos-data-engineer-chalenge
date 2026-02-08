# Tests for application constants.

from source_api.application import constants


class TestConstants:
    def test_when_constants_are_loaded_should_match_expected_values(self):
        # Arrange

        # Act

        # Assert
        assert constants.ALLOWED_SIGNAL_NAMES == (
            "wind_speed",
            "power",
            "ambient_temperature",
        )

