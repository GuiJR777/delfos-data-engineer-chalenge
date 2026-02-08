# Tests for ApplicationLifecycle.

from unittest.mock import MagicMock

from source_api.api.lifecycle import ApplicationLifecycle


class TestInit:
    def test_when_instance_is_created_should_store_manager(self):
        # Arrange

        manager = MagicMock()

        # Act

        lifecycle = ApplicationLifecycle(manager)

        # Assert

        assert lifecycle._database_engine_manager == manager


class TestDoStartup:
    def test_when_called_should_start_manager(self):
        # Arrange

        manager = MagicMock()
        lifecycle = ApplicationLifecycle(manager)

        # Act

        lifecycle.do_startup()

        # Assert

        manager.do_startup.assert_called_once_with()


class TestDoShutdown:
    def test_when_called_should_shutdown_manager(self):
        # Arrange

        manager = MagicMock()
        lifecycle = ApplicationLifecycle(manager)

        # Act

        lifecycle.do_shutdown()

        # Assert

        manager.do_shutdown.assert_called_once_with()

