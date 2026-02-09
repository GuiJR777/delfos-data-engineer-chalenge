# Tests for EtlSettings.

from unittest.mock import MagicMock

import etl.settings as settings_module
from etl.constants import (
    API_BASE_URL_ENV_NAME,
    API_LIMIT_ENV_NAME,
    API_OFFSET_ENV_NAME,
    API_RETRY_ATTEMPTS_ENV_NAME,
    API_TIMEOUT_SECONDS_ENV_NAME,
    DEFAULT_API_BASE_URL,
    DEFAULT_API_LIMIT,
    DEFAULT_API_OFFSET,
    DEFAULT_API_RETRY_ATTEMPTS,
    DEFAULT_API_TIMEOUT_SECONDS,
    DEFAULT_LOG_LEVEL,
    LOG_LEVEL_ENV_NAME,
)
from etl.settings import EtlSettings


class TestGetApiBaseUrl:
    def test_when_env_is_set_should_return_value(self, monkeypatch):
        # Arrange

        expected_url = "http://api.local"

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(API_BASE_URL_ENV_NAME, expected_url)

        settings = EtlSettings()

        # Act

        result = settings.get_api_base_url()

        # Assert

        assert result == expected_url

    def test_when_env_is_missing_should_return_default(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(API_BASE_URL_ENV_NAME, raising=False)

        settings = EtlSettings()

        # Act

        result = settings.get_api_base_url()

        # Assert

        assert result == DEFAULT_API_BASE_URL


class TestGetApiTimeoutSeconds:
    def test_when_env_is_set_should_return_value(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(API_TIMEOUT_SECONDS_ENV_NAME, "12.5")

        settings = EtlSettings()

        # Act

        result = settings.get_api_timeout_seconds()

        # Assert

        assert result == 12.5

    def test_when_env_is_missing_should_return_default(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(API_TIMEOUT_SECONDS_ENV_NAME, raising=False)

        settings = EtlSettings()

        # Act

        result = settings.get_api_timeout_seconds()

        # Assert

        assert result == DEFAULT_API_TIMEOUT_SECONDS


class TestGetApiRetryAttempts:
    def test_when_env_is_set_should_return_value(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(API_RETRY_ATTEMPTS_ENV_NAME, "3")

        settings = EtlSettings()

        # Act

        result = settings.get_api_retry_attempts()

        # Assert

        assert result == 3

    def test_when_env_is_missing_should_return_default(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(API_RETRY_ATTEMPTS_ENV_NAME, raising=False)

        settings = EtlSettings()

        # Act

        result = settings.get_api_retry_attempts()

        # Assert

        assert result == DEFAULT_API_RETRY_ATTEMPTS


class TestGetApiLimit:
    def test_when_env_is_set_should_return_value(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(API_LIMIT_ENV_NAME, "1234")

        settings = EtlSettings()

        # Act

        result = settings.get_api_limit()

        # Assert

        assert result == 1234

    def test_when_env_is_missing_should_return_default(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(API_LIMIT_ENV_NAME, raising=False)

        settings = EtlSettings()

        # Act

        result = settings.get_api_limit()

        # Assert

        assert result == DEFAULT_API_LIMIT


class TestGetApiOffset:
    def test_when_env_is_set_should_return_value(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(API_OFFSET_ENV_NAME, "42")

        settings = EtlSettings()

        # Act

        result = settings.get_api_offset()

        # Assert

        assert result == 42

    def test_when_env_is_missing_should_return_default(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(API_OFFSET_ENV_NAME, raising=False)

        settings = EtlSettings()

        # Act

        result = settings.get_api_offset()

        # Assert

        assert result == DEFAULT_API_OFFSET


class TestGetLogLevel:
    def test_when_env_is_set_should_return_value(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.setenv(LOG_LEVEL_ENV_NAME, "DEBUG")

        settings = EtlSettings()

        # Act

        result = settings.get_log_level()

        # Assert

        assert result == "DEBUG"

    def test_when_env_is_missing_should_return_default(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(settings_module, "load_dotenv", MagicMock())
        monkeypatch.delenv(LOG_LEVEL_ENV_NAME, raising=False)

        settings = EtlSettings()

        # Act

        result = settings.get_log_level()

        # Assert

        assert result == DEFAULT_LOG_LEVEL

