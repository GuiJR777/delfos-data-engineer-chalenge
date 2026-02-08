# Configuracoes do banco alvo.

import os

from dotenv import load_dotenv

from etl.target_database.constants import (
    DATABASE_URL_ENV_NAME,
    MISSING_TARGET_DATABASE_URL_MESSAGE,
    TARGET_DATABASE_URL_ENV_NAME,
)


class TargetDatabaseSettings:
    def __init__(self) -> None:
        load_dotenv()

    def get_target_database_url(self) -> str:
        target_database_url = os.getenv(TARGET_DATABASE_URL_ENV_NAME)
        has_target_database_url = bool(target_database_url)
        if has_target_database_url:
            return target_database_url

        fallback_database_url = os.getenv(DATABASE_URL_ENV_NAME)
        has_fallback_database_url = bool(fallback_database_url)
        if has_fallback_database_url:
            return fallback_database_url

        raise RuntimeError(MISSING_TARGET_DATABASE_URL_MESSAGE)

