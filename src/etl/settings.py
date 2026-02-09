# Configuracoes do ETL.

import os

from dotenv import load_dotenv

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


class EtlSettings:
    def __init__(self) -> None:
        load_dotenv()

    def get_api_base_url(self) -> str:
        return os.getenv(API_BASE_URL_ENV_NAME, DEFAULT_API_BASE_URL)

    def get_api_timeout_seconds(self) -> float:
        timeout_seconds = os.getenv(API_TIMEOUT_SECONDS_ENV_NAME)
        has_timeout_seconds = bool(timeout_seconds)
        if not has_timeout_seconds:
            return DEFAULT_API_TIMEOUT_SECONDS

        return float(timeout_seconds)

    def get_api_retry_attempts(self) -> int:
        retry_attempts = os.getenv(API_RETRY_ATTEMPTS_ENV_NAME)
        has_retry_attempts = bool(retry_attempts)
        if not has_retry_attempts:
            return DEFAULT_API_RETRY_ATTEMPTS

        return int(retry_attempts)

    def get_api_limit(self) -> int:
        api_limit = os.getenv(API_LIMIT_ENV_NAME)
        has_api_limit = bool(api_limit)
        if not has_api_limit:
            return DEFAULT_API_LIMIT

        return int(api_limit)

    def get_api_offset(self) -> int:
        api_offset = os.getenv(API_OFFSET_ENV_NAME)
        has_api_offset = bool(api_offset)
        if not has_api_offset:
            return DEFAULT_API_OFFSET

        return int(api_offset)

    def get_log_level(self) -> str:
        return os.getenv(LOG_LEVEL_ENV_NAME, DEFAULT_LOG_LEVEL)

