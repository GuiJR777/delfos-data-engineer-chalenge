# Tests for DataQueryValidationError.

from source_api.application.exceptions import DataQueryValidationError


class TestInit:
    def test_when_exception_is_created_should_store_message(self):
        # Arrange

        message = "invalid query"

        # Act

        error = DataQueryValidationError(message)

        # Assert

        assert str(error) == message

