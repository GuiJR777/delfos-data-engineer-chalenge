# Tests for source_api package init.

import source_api as source_api_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = source_api_module

        # Assert

        assert result is not None

