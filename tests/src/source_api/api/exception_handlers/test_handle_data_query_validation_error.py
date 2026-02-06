# Tests for exception handlers.

from unittest.mock import MagicMock

import source_api.api.exception_handlers as handlers


class TestHandleDataQueryValidationError:
    def test_when_called_should_return_json_response(self, monkeypatch):
        # Arrange

        request = MagicMock()
        request.url.path = "/data"
        exception = Exception("invalid")
        logger = MagicMock()
        json_response_instance = MagicMock()
        json_response_class = MagicMock(return_value=json_response_instance)
        monkeypatch.setattr(handlers, "logger", logger)
        monkeypatch.setattr(handlers, "JSONResponse", json_response_class)

        # Act

        result = handlers.handle_data_query_validation_error(
            request,
            exception,
        )

        # Assert

        logger.error.assert_called_once_with(
            "Data query validation failed",
            extra={
                "detail": "invalid",
                "path": "/data",
            },
        )
        json_response_class.assert_called_once_with(
            status_code=handlers.HTTP_BAD_REQUEST,
            content={"detail": "invalid"},
        )
        assert result == json_response_instance

