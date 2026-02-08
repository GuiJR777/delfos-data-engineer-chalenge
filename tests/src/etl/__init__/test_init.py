# Tests for etl package init.

import etl as etl_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = etl_module

        # Assert

        assert result is not None

