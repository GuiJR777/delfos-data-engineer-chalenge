# Tests for orchestration assets package init.

import orchestration.assets as assets_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = assets_module

        # Assert

        assert result is not None

