# Tests for DagsterDefinitionsFactory.

from dagster import Definitions

from orchestration.constants import ETL_JOB_NAME, ETL_SCHEDULE_NAME
from orchestration.definitions import DagsterDefinitionsFactory


class TestGetDefinitions:
    def test_when_called_should_build_definitions(self):
        # Arrange

        factory = DagsterDefinitionsFactory()

        # Act

        result = factory.get_definitions()

        # Assert

        assert isinstance(result, Definitions)
        assert result.get_job_def(ETL_JOB_NAME) is not None
        assert result.get_schedule_def(ETL_SCHEDULE_NAME) is not None

