# Tests for DailyEtlScheduleFactory.

from orchestration.constants import DAILY_SCHEDULE_CRON, ETL_SCHEDULE_NAME
from orchestration.jobs import DailyEtlJobFactory
from orchestration.schedules import DailyEtlScheduleFactory


class TestGetSchedule:
    def test_when_called_should_build_schedule(self):
        # Arrange
        job = DailyEtlJobFactory().get_job()
        schedule_factory = DailyEtlScheduleFactory(job)

        # Act

        result = schedule_factory.get_schedule()

        # Assert

        assert result.name == ETL_SCHEDULE_NAME
        assert result.cron_schedule == DAILY_SCHEDULE_CRON
