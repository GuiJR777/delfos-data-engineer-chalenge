# Tests for orchestration package init.

import orchestration as orchestration_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = orchestration_module

        # Assert

        assert result is not None

