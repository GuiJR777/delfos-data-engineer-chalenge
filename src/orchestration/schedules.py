# Schedules do Dagster.

from dagster import JobDefinition, ScheduleDefinition

from orchestration.constants import DAILY_SCHEDULE_CRON, ETL_SCHEDULE_NAME


class DailyEtlScheduleFactory:
    def __init__(self, job: JobDefinition) -> None:
        self._job = job

    def get_schedule(self) -> ScheduleDefinition:
        return ScheduleDefinition(
            name=ETL_SCHEDULE_NAME,
            cron_schedule=DAILY_SCHEDULE_CRON,
            job=self._job,
        )

