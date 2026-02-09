# Tests for SourceApiClient.

from unittest.mock import MagicMock

import httpx
import pytest

import etl.source_api_client as client_module
from etl.source_api_client import SourceApiClient


def _build_response(payload):
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


class TestDoClose:
    def test_when_called_should_close_http_client(self, monkeypatch):
        # Arrange

        http_client = MagicMock()
        client_class = MagicMock(return_value=http_client)
        monkeypatch.setattr(client_module.httpx, "Client", client_class)

        client = SourceApiClient(
            base_url="http://localhost",
            timeout_seconds=1.0,
            retry_attempts=1,
            api_limit=10,
            api_offset=0,
        )

        # Act

        client.do_close()

        # Assert

        http_client.close.assert_called_once_with()


class TestDoFetchData:
    def test_when_multiple_pages_should_fetch_all(self, monkeypatch):
        # Arrange

        first_response = _build_response(
            [{"timestamp": "2024-01-01T00:00:00"}]
            + [{"timestamp": "2024-01-01T00:01:00"}]
        )
        second_response = _build_response(
            [{"timestamp": "2024-01-01T00:02:00"}]
        )

        http_client = MagicMock()
        http_client.get.side_effect = [first_response, second_response]

        client_class = MagicMock(return_value=http_client)
        monkeypatch.setattr(client_module.httpx, "Client", client_class)

        client = SourceApiClient(
            base_url="http://localhost",
            timeout_seconds=1.0,
            retry_attempts=1,
            api_limit=2,
            api_offset=0,
        )

        # Act

        result = client.do_fetch_data(
            start_timestamp="2024-01-01T00:00:00",
            end_timestamp="2024-01-02T00:00:00",
            signal_names=("wind_speed", "power"),
        )

        # Assert

        assert len(result) == 3
        assert http_client.get.call_count == 2


class TestDoFetchPage:
    def test_when_response_is_valid_should_return_payload(
        self,
        monkeypatch,
    ):
        # Arrange

        response = _build_response(
            [{"timestamp": "2024-01-01T00:00:00"}]
        )

        http_client = MagicMock()
        http_client.get.return_value = response

        client_class = MagicMock(return_value=http_client)
        monkeypatch.setattr(client_module.httpx, "Client", client_class)

        client = SourceApiClient(
            base_url="http://localhost",
            timeout_seconds=1.0,
            retry_attempts=1,
            api_limit=10,
            api_offset=0,
        )

        # Act

        result = client._do_fetch_page(
            start_timestamp="2024-01-01T00:00:00",
            end_timestamp="2024-01-02T00:00:00",
            signal_names=("wind_speed", "power"),
            limit_value=10,
            offset_value=0,
        )

        # Assert

        assert result == [{"timestamp": "2024-01-01T00:00:00"}]

    def test_when_payload_is_not_list_should_raise_error(
        self,
        monkeypatch,
    ):
        # Arrange

        response = _build_response({"invalid": "payload"})

        http_client = MagicMock()
        http_client.get.return_value = response

        client_class = MagicMock(return_value=http_client)
        monkeypatch.setattr(client_module.httpx, "Client", client_class)

        client = SourceApiClient(
            base_url="http://localhost",
            timeout_seconds=1.0,
            retry_attempts=1,
            api_limit=10,
            api_offset=0,
        )

        # Act

        with pytest.raises(RuntimeError):
            client._do_fetch_page(
                start_timestamp="2024-01-01T00:00:00",
                end_timestamp="2024-01-02T00:00:00",
                signal_names=("wind_speed", "power"),
                limit_value=10,
                offset_value=0,
            )

        # Assert

    def test_when_request_fails_should_retry_and_raise(
        self,
        monkeypatch,
    ):
        # Arrange

        request = MagicMock()
        request_error = httpx.RequestError(
            "boom",
            request=request,
        )

        http_client = MagicMock()
        http_client.get.side_effect = [
            request_error,
            request_error,
        ]

        client_class = MagicMock(return_value=http_client)
        monkeypatch.setattr(client_module.httpx, "Client", client_class)

        client = SourceApiClient(
            base_url="http://localhost",
            timeout_seconds=1.0,
            retry_attempts=2,
            api_limit=10,
            api_offset=0,
        )

        # Act

        with pytest.raises(RuntimeError):
            client._do_fetch_page(
                start_timestamp="2024-01-01T00:00:00",
                end_timestamp="2024-01-02T00:00:00",
                signal_names=("wind_speed", "power"),
                limit_value=10,
                offset_value=0,
            )

        # Assert

