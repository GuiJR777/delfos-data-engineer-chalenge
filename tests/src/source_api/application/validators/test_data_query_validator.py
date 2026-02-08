# Tests for DataQueryValidator.

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from source_api.application.exceptions import DataQueryValidationError
from source_api.application.validators import DataQueryValidator
from source_api.application import validators


class TestInit:
    def test_when_instance_is_created_should_store_allowed_signals(self):
        # Arrange

        allowed_signal_names = ["wind_speed", "power"]
        expected_signal_names = {"wind_speed", "power"}

        # Act

        validator = DataQueryValidator(allowed_signal_names)

        # Assert

        assert validator._allowed_signal_names == expected_signal_names


class TestDoValidate:
    def test_when_start_is_after_end_should_raise_error(self):
        # Arrange

        validator = DataQueryValidator(["wind_speed"])
        data_query = MagicMock()
        data_query.start_timestamp = datetime(2024, 1, 2, 0, 0, 0)
        data_query.end_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        data_query.signal_names = ["wind_speed"]

        # Act

        with pytest.raises(DataQueryValidationError) as excinfo:
            validator.do_validate(data_query)

        # Assert

        assert str(excinfo.value) == validators.START_END_INVALID_MESSAGE

    def test_when_signals_are_empty_should_raise_error(self):
        # Arrange

        validator = DataQueryValidator(["wind_speed"])
        data_query = MagicMock()
        data_query.start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        data_query.end_timestamp = datetime(2024, 1, 2, 0, 0, 0)
        data_query.signal_names = []

        # Act

        with pytest.raises(DataQueryValidationError) as excinfo:
            validator.do_validate(data_query)

        # Assert

        assert str(excinfo.value) == validators.SIGNALS_EMPTY_MESSAGE

    def test_when_signals_are_invalid_should_raise_error(self):
        # Arrange

        validator = DataQueryValidator(["wind_speed"])
        data_query = MagicMock()
        data_query.start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        data_query.end_timestamp = datetime(2024, 1, 2, 0, 0, 0)
        data_query.signal_names = ["invalid"]

        # Act

        with pytest.raises(DataQueryValidationError) as excinfo:
            validator.do_validate(data_query)

        # Assert

        expected_message = (
            validators.INVALID_SIGNALS_MESSAGE_PREFIX
            + "wind_speed"
            + validators.INVALID_SIGNALS_MESSAGE_SUFFIX
        )
        assert str(excinfo.value) == expected_message

    def test_when_query_is_valid_should_not_raise_error(self):
        # Arrange

        validator = DataQueryValidator(["wind_speed"])
        data_query = MagicMock()
        data_query.start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        data_query.end_timestamp = datetime(2024, 1, 2, 0, 0, 0)
        data_query.signal_names = ["wind_speed"]

        # Act

        result = validator.do_validate(data_query)

        # Assert

        assert result is None


class TestGetInvalidSignalNames:
    @pytest.mark.parametrize(
        "signal_names, expected",
        [
            (["wind_speed"], []),
            (["wind_speed", "invalid"], ["invalid"]),
            (["invalid", "another"], ["invalid", "another"]),
        ],
    )
    def test_when_signals_are_provided_should_return_invalid_list(
        self,
        signal_names,
        expected,
    ):
        # Arrange

        validator = DataQueryValidator(["wind_speed", "power"])

        # Act

        result = validator.get_invalid_signal_names(signal_names)

        # Assert

        assert result == expected

