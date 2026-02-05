# Configuracoes de ambiente da Source API.

import os

from dotenv import load_dotenv

SOURCE_DATABASE_URL_ENV_NAME: str = "SOURCE_DATABASE_URL"
DATABASE_URL_ENV_NAME: str = "DATABASE_URL"

MISSING_DATABASE_URL_MESSAGE: str = "SOURCE_DATABASE_URL is not set"


class ApplicationSettings:
    def __init__(self) -> None:
        load_dotenv()

    def get_source_database_url(self) -> str:
        source_database_url = os.getenv(SOURCE_DATABASE_URL_ENV_NAME)
        has_source_database_url = bool(source_database_url)
        if has_source_database_url:
            return source_database_url

        fallback_database_url = os.getenv(DATABASE_URL_ENV_NAME)
        has_fallback_database_url = bool(fallback_database_url)
        if has_fallback_database_url:
            return fallback_database_url

        raise RuntimeError(MISSING_DATABASE_URL_MESSAGE)

