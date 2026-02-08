# Tests for Base model.

from sqlalchemy.orm import DeclarativeBase

from etl.target_database.models import Base


class TestBase:
    def test_when_base_is_defined_should_inherit_from_declarative_base(
        self,
    ):
        # Arrange

        # Act

        result = issubclass(Base, DeclarativeBase)

        # Assert

        assert result is True

