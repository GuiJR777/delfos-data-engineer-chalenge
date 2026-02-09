# Tests for orchestration constants.

from orchestration import constants


class TestConstants:
    def test_when_constants_are_loaded_should_match_expected_values(self):
        # Arrange

        # Act

        # Assert
        assert constants.PARTITION_START_DATE == "2024-01-01"
        assert constants.DAILY_SCHEDULE_CRON == "0 1 * * *"
        assert constants.ETL_ASSET_NAME == "daily_etl"
        assert constants.ETL_JOB_NAME == "daily_etl_job"
        assert constants.ETL_SCHEDULE_NAME == "daily_etl_schedule"
        assert constants.SOURCE_API_RESOURCE_KEY == "source_api_client"
        assert constants.TARGET_DB_ENGINE_RESOURCE_KEY == "target_db_engine"

