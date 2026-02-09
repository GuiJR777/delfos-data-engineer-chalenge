# Tests for SourceApiClientResourceFactory.

from unittest.mock import MagicMock

import orchestration.resources as resources_module
from orchestration.resources import SourceApiClientResourceFactory


class TestGetClient:
    def test_when_called_should_build_source_api_client(
        self,
        monkeypatch,
    ):
        # Arrange

        settings = MagicMock()
        settings.get_api_base_url.return_value = "http://api"
        settings.get_api_timeout_seconds.return_value = 2.0
        settings.get_api_retry_attempts.return_value = 2
        settings.get_api_limit.return_value = 100
        settings.get_api_offset.return_value = 10

        client_instance = MagicMock()
        client_class = MagicMock(return_value=client_instance)
        monkeypatch.setattr(
            resources_module,
            "SourceApiClient",
            client_class,
        )

        factory = SourceApiClientResourceFactory(settings)

        # Act

        result = factory.get_client()

        # Assert

        assert result == client_instance
        client_class.assert_called_once_with(
            base_url="http://api",
            timeout_seconds=2.0,
            retry_attempts=2,
            api_limit=100,
            api_offset=10,
        )

