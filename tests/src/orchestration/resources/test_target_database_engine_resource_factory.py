# Tests for TargetDatabaseEngineResourceFactory.

from unittest.mock import MagicMock

import orchestration.resources as resources_module
from orchestration.resources import TargetDatabaseEngineResourceFactory


class TestGetEngineManager:
    def test_when_called_should_build_engine_manager(
        self,
        monkeypatch,
    ):
        # Arrange

        settings = MagicMock()
        engine_manager = MagicMock()

        engine_manager_class = MagicMock(return_value=engine_manager)
        monkeypatch.setattr(
            resources_module,
            "TargetDatabaseEngineManager",
            engine_manager_class,
        )

        factory = TargetDatabaseEngineResourceFactory(settings)

        # Act

        result = factory.get_engine_manager()

        # Assert

        assert result == engine_manager
        engine_manager_class.assert_called_once_with(settings)

