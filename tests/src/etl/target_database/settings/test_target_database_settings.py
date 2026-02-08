# Tests for TargetDatabaseSettings.

from unittest.mock import MagicMock

import pytest

import etl.target_database.settings as settings_module
from etl.target_database.constants import (
    DATABASE_URL_ENV_NAME,
    MISSING_TARGET_DATABASE_URL_MESSAGE,
    TARGET_DATABASE_URL_ENV_NAME,
)
from etl.target_database.settings import TargetDatabaseSettings


class TestGetTargetDatabaseUrl:
    def test_when_target_database_url_is_set_should_return_value(
        self,
        monkeypatch,
    ):
        # Arrange

        database_url = "postgresql://user@host/target"

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(TARGET_DATABASE_URL_ENV_NAME, database_url)
        monkeypatch.delenv(DATABASE_URL_ENV_NAME, raising=False)

        settings = TargetDatabaseSettings()

        # Act

        result = settings.get_target_database_url()

        # Assert

        assert result == database_url

    def test_when_target_database_url_is_missing_should_use_fallback(
        self,
        monkeypatch,
    ):
        # Arrange

        fallback_url = "postgresql://user@host/fallback"

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(TARGET_DATABASE_URL_ENV_NAME, raising=False)
        monkeypatch.setenv(DATABASE_URL_ENV_NAME, fallback_url)

        settings = TargetDatabaseSettings()

        # Act

        result = settings.get_target_database_url()

        # Assert

        assert result == fallback_url

    def test_when_no_database_url_is_set_should_raise_error(
        self,
        monkeypatch,
    ):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(TARGET_DATABASE_URL_ENV_NAME, raising=False)
        monkeypatch.delenv(DATABASE_URL_ENV_NAME, raising=False)

        settings = TargetDatabaseSettings()

        # Act

        with pytest.raises(RuntimeError) as error:
            settings.get_target_database_url()

        # Assert

        assert str(error.value) == MISSING_TARGET_DATABASE_URL_MESSAGE

