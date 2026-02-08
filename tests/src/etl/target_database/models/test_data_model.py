# Tests for DataModel.

from etl.target_database.constants import (
    DATA_TABLE_NAME,
    DATA_UNIQUE_CONSTRAINT_NAME,
)
from etl.target_database.models import DataModel

FIRST_ITEM_INDEX: int = 0


class TestDataModelDefinition:
    def test_when_model_is_defined_should_set_table_name(self):
        # Arrange

        # Act

        result = DataModel.__tablename__

        # Assert

        assert result == DATA_TABLE_NAME

    def test_when_model_is_defined_should_set_unique_constraint(self):
        # Arrange

        # Act

        constraint = DataModel.__table_args__[FIRST_ITEM_INDEX]

        # Assert

        assert constraint.name == DATA_UNIQUE_CONSTRAINT_NAME

    def test_when_model_is_defined_should_set_primary_keys(self):
        # Arrange

        # Act

        timestamp_column = DataModel.__table__.c.timestamp
        signal_id_column = DataModel.__table__.c.signal_id

        # Assert

        assert timestamp_column.primary_key is True
        assert signal_id_column.primary_key is True

    def test_when_model_is_defined_should_require_value(self):
        # Arrange

        # Act

        value_column = DataModel.__table__.c.value

        # Assert

        assert value_column.nullable is False

