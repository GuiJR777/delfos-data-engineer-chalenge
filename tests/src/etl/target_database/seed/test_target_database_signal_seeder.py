# Tests for TargetDatabaseSignalSeeder.

from unittest.mock import MagicMock

from etl.target_database.constants import DEFAULT_SIGNAL_NAMES
from etl.target_database.seed import TargetDatabaseSignalSeeder


class TestGetSignalNames:
    def test_when_no_custom_names_should_return_defaults(self):
        # Arrange

        session_factory = MagicMock()

        # Act

        seeder = TargetDatabaseSignalSeeder(session_factory)
        result = seeder.get_signal_names()

        # Assert

        assert result == DEFAULT_SIGNAL_NAMES

    def test_when_custom_names_are_provided_should_return_custom(self):
        # Arrange

        session_factory = MagicMock()
        custom_names = ("custom_mean", "custom_max")

        # Act

        seeder = TargetDatabaseSignalSeeder(
            session_factory,
            signal_names=custom_names,
        )
        result = seeder.get_signal_names()

        # Assert

        assert result == custom_names


class TestDoSeedSignals:
    def test_when_signal_names_are_empty_should_skip_session(self):
        # Arrange

        session_factory = MagicMock()
        seeder = TargetDatabaseSignalSeeder(
            session_factory,
            signal_names=(),
        )

        # Act

        seeder.do_seed_signals()

        # Assert

        session_factory.get_session.assert_not_called()

    def test_when_signal_names_exist_should_execute_and_commit(self):
        # Arrange

        session = MagicMock()
        session_factory = MagicMock()
        session_factory.get_session.return_value = session

        seeder = TargetDatabaseSignalSeeder(
            session_factory,
            signal_names=("wind_speed_mean",),
        )

        # Act

        seeder.do_seed_signals()

        # Assert

        session_factory.get_session.assert_called_once_with()
        session.execute.assert_called_once()
        session.commit.assert_called_once_with()
        session.close.assert_called_once_with()

