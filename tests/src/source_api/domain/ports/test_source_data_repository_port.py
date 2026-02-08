# Tests for SourceDataRepositoryPort.

from datetime import datetime

import pytest

from source_api.domain.ports import SourceDataRepositoryPort


class FakeRepository(SourceDataRepositoryPort):
    def get_data_rows(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime,
        signal_names: list[str],
        limit: int,
        offset: int,
    ) -> list[object]:
        return []


class TestGetDataRows:
    def test_when_instantiating_abstract_class_should_raise_type_error(self):
        # Arrange

        # Act

        with pytest.raises(TypeError) as excinfo:
            SourceDataRepositoryPort()

        # Assert

        assert "abstract" in str(excinfo.value)

    def test_when_subclass_implements_method_should_return_data(self):
        # Arrange

        repository = FakeRepository()
        start_timestamp = datetime(2024, 1, 1, 0, 0, 0)
        end_timestamp = datetime(2024, 1, 1, 1, 0, 0)
        signal_names = ["wind_speed"]

        # Act

        result = repository.get_data_rows(
            start_timestamp,
            end_timestamp,
            signal_names,
            10,
            0,
        )

        # Assert

        assert result == []

