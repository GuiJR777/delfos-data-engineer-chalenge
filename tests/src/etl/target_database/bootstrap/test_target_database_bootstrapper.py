# Tests for TargetDatabaseBootstrapper.

from unittest.mock import MagicMock

from etl.target_database.bootstrap import TargetDatabaseBootstrapper


class TestDoBootstrap:
    def test_when_called_should_create_schema_and_seed_signals(self):
        # Arrange

        schema_manager = MagicMock()
        signal_seeder = MagicMock()

        bootstrapper = TargetDatabaseBootstrapper(
            schema_manager,
            signal_seeder,
        )

        # Act

        bootstrapper.do_bootstrap()

        # Assert

        schema_manager.do_create_schema.assert_called_once_with()
        signal_seeder.do_seed_signals.assert_called_once_with()

