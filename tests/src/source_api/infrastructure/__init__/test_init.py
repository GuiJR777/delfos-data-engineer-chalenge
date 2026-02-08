# Tests for infrastructure package init.

import source_api.infrastructure as infrastructure_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = infrastructure_module

        # Assert

        assert result is not None

