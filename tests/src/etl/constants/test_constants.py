# Tests for ETL constants.

from etl import constants


class TestConstants:
    def test_when_constants_are_loaded_should_match_expected_values(self):
        # Arrange

        # Act

        # Assert
        assert constants.API_BASE_URL_ENV_NAME == "API_BASE_URL"
        assert constants.API_TIMEOUT_SECONDS_ENV_NAME == "API_TIMEOUT_SECONDS"
        assert constants.API_RETRY_ATTEMPTS_ENV_NAME == "API_RETRY_ATTEMPTS"
        assert constants.API_LIMIT_ENV_NAME == "API_LIMIT"
        assert constants.API_OFFSET_ENV_NAME == "API_OFFSET"
        assert constants.LOG_LEVEL_ENV_NAME == "LOG_LEVEL"
        assert constants.DEFAULT_API_BASE_URL == "http://localhost:8000"
        assert constants.DEFAULT_API_TIMEOUT_SECONDS == 15.0
        assert constants.DEFAULT_API_RETRY_ATTEMPTS == 2
        assert constants.DEFAULT_API_LIMIT == 50_000
        assert constants.DEFAULT_API_OFFSET == 0
        assert constants.DEFAULT_LOG_LEVEL == "INFO"
        assert constants.API_DATA_PATH == "/data"
        assert constants.DATE_FORMAT == "%Y-%m-%d"
        assert constants.TIMESTAMP_COLUMN_NAME == "timestamp"
        assert constants.SIGNAL_NAME_COLUMN_NAME == "signal_name"
        assert constants.VALUE_COLUMN_NAME == "value"
        assert constants.SOURCE_SIGNAL_NAMES == ("wind_speed", "power")
        assert constants.AGGREGATION_FUNCTIONS == (
            "mean",
            "min",
            "max",
            "std",
        )
        assert constants.RESAMPLE_WINDOW_MINUTES == 10
        assert constants.RESAMPLE_WINDOW_SUFFIX == "min"
        assert constants.DEFAULT_INSERT_BATCH_SIZE == 1000

