# Tests for domain package init.

import source_api.domain as domain_module


class TestInit:
    def test_when_module_is_imported_should_be_available(self):
        # Arrange

        # Act

        result = domain_module

        # Assert

        assert result is not None

