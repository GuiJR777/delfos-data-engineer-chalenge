# Tests for target database constants.

from etl.target_database import constants


class TestConstants:
    def test_when_constants_are_loaded_should_match_expected_values(self):
        # Arrange

        # Act

        # Assert
        assert (
            constants.TARGET_DATABASE_URL_ENV_NAME
            == "TARGET_DATABASE_URL"
        )
        assert constants.DATABASE_URL_ENV_NAME == "DATABASE_URL"
        assert (
            constants.MISSING_TARGET_DATABASE_URL_MESSAGE
            == "TARGET_DATABASE_URL is not set"
        )
        assert constants.SIGNAL_TABLE_NAME == "signal"
        assert constants.DATA_TABLE_NAME == "data"
        assert constants.SIGNAL_NAME_MAX_LENGTH == 128
        assert (
            constants.DATA_UNIQUE_CONSTRAINT_NAME
            == "uq_data_timestamp_signal"
        )
        assert constants.DEFAULT_SIGNAL_NAMES == (
            "wind_speed_mean",
            "wind_speed_min",
            "wind_speed_max",
            "wind_speed_std",
            "power_mean",
            "power_min",
            "power_max",
            "power_std",
        )

