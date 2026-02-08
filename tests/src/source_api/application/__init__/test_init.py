# Tests for application package init.

import source_api.application as application_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = application_module

        # Assert

        assert result is not None

