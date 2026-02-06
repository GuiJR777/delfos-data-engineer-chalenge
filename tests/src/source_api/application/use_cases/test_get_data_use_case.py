# Tests for GetDataUseCase.

from unittest.mock import MagicMock

from source_api.application.use_cases import GetDataUseCase


class TestInit:
    def test_when_instance_is_created_should_store_dependencies(self):
        # Arrange

        repository = MagicMock()
        validator = MagicMock()

        # Act

        use_case = GetDataUseCase(repository, validator)

        # Assert

        assert use_case._repository == repository
        assert use_case._validator == validator


class TestGetDataRows:
    def test_when_called_should_validate_and_fetch_data(self):
        # Arrange

        repository = MagicMock()
        validator = MagicMock()
        use_case = GetDataUseCase(repository, validator)
        data_query = MagicMock()
        data_query.start_timestamp = "start"
        data_query.end_timestamp = "end"
        data_query.signal_names = ["wind_speed"]
        data_query.limit = 10
        data_query.offset = 0
        repository.get_data_rows.return_value = ["row"]

        # Act

        result = use_case.get_data_rows(data_query)

        # Assert

        validator.do_validate.assert_called_once_with(data_query)
        repository.get_data_rows.assert_called_once_with(
            data_query.start_timestamp,
            data_query.end_timestamp,
            data_query.signal_names,
            data_query.limit,
            data_query.offset,
        )
        assert result == ["row"]

