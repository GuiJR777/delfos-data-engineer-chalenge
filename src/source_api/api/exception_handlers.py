# Handlers de excecao da API.

import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from source_api.application.exceptions import DataQueryValidationError

HTTP_BAD_REQUEST: int = status.HTTP_400_BAD_REQUEST
LOGGER_NAME: str = "source_api"

logger = logging.getLogger(LOGGER_NAME)


def handle_data_query_validation_error(
    request: Request,
    exception: DataQueryValidationError,
) -> JSONResponse:
    logger.error(
        "Data query validation failed",
        extra={
            "detail": str(exception),
            "path": request.url.path,
        },
    )
    return JSONResponse(
        status_code=HTTP_BAD_REQUEST,
        content={"detail": str(exception)},
    )

