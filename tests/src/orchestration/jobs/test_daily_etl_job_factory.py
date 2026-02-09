# Tests for DailyEtlJobFactory.

from orchestration.constants import ETL_JOB_NAME
from orchestration.jobs import DailyEtlJobFactory


class TestGetJob:
    def test_when_called_should_build_job(self):
        # Arrange

        factory = DailyEtlJobFactory()

        # Act

        result = factory.get_job()

        # Assert

        assert result.name == ETL_JOB_NAME

