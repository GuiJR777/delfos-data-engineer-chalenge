# Tests for ApplicationSettings.

from unittest.mock import MagicMock

import pytest

import source_api.infrastructure.settings as settings_module


class TestInit:
    def test_when_instance_is_created_should_load_dotenv(self, monkeypatch):
        # Arrange

        load_dotenv = MagicMock()
        monkeypatch.setattr(settings_module, "load_dotenv", load_dotenv)

        # Act

        settings_module.ApplicationSettings()

        # Assert

        load_dotenv.assert_called_once_with()


class TestGetSourceDatabaseUrl:
    def test_when_source_database_url_is_set_should_return_value(
        self,
        monkeypatch,
    ):
        # Arrange

        expected_url = "postgresql://user:pass@host:5432/db"
        load_dotenv = MagicMock()
        monkeypatch.setattr(settings_module, "load_dotenv", load_dotenv)
        monkeypatch.setenv(
            settings_module.SOURCE_DATABASE_URL_ENV_NAME,
            expected_url,
        )
        monkeypatch.delenv(
            settings_module.DATABASE_URL_ENV_NAME,
            raising=False,
        )
        settings = settings_module.ApplicationSettings()

        # Act

        result = settings.get_source_database_url()

        # Assert

        assert result == expected_url

    def test_when_fallback_database_url_is_set_should_return_value(
        self,
        monkeypatch,
    ):
        # Arrange

        expected_url = "postgresql://user:pass@host:5432/db"
        load_dotenv = MagicMock()
        monkeypatch.setattr(settings_module, "load_dotenv", load_dotenv)
        monkeypatch.delenv(
            settings_module.SOURCE_DATABASE_URL_ENV_NAME,
            raising=False,
        )
        monkeypatch.setenv(
            settings_module.DATABASE_URL_ENV_NAME,
            expected_url,
        )
        settings = settings_module.ApplicationSettings()

        # Act

        result = settings.get_source_database_url()

        # Assert

        assert result == expected_url

    def test_when_no_database_url_is_set_should_raise_error(
        self,
        monkeypatch,
    ):
        # Arrange

        load_dotenv = MagicMock()
        monkeypatch.setattr(settings_module, "load_dotenv", load_dotenv)
        monkeypatch.delenv(
            settings_module.SOURCE_DATABASE_URL_ENV_NAME,
            raising=False,
        )
        monkeypatch.delenv(
            settings_module.DATABASE_URL_ENV_NAME,
            raising=False,
        )
        settings = settings_module.ApplicationSettings()

        # Act

        with pytest.raises(RuntimeError) as excinfo:
            settings.get_source_database_url()

        # Assert

        assert str(excinfo.value) == settings_module.MISSING_DATABASE_URL_MESSAGE

