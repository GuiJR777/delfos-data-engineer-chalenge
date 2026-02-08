# Tests for target_database package init.

import etl.target_database as target_database_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = target_database_module

        # Assert

        assert result is not None

