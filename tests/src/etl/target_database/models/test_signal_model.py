# Tests for SignalModel.

from etl.target_database.constants import (
    SIGNAL_NAME_MAX_LENGTH,
    SIGNAL_TABLE_NAME,
)
from etl.target_database.models import SignalModel


class TestSignalModelDefinition:
    def test_when_model_is_defined_should_set_table_name(self):
        # Arrange

        # Act

        result = SignalModel.__tablename__

        # Assert

        assert result == SIGNAL_TABLE_NAME

    def test_when_model_is_defined_should_set_name_column(self):
        # Arrange

        # Act

        name_column = SignalModel.__table__.c.name

        # Assert

        assert name_column.unique is True
        assert name_column.nullable is False
        assert name_column.type.length == SIGNAL_NAME_MAX_LENGTH

