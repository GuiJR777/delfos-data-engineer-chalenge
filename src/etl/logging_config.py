# Configuracao de logs do ETL.

import logging

from etl.settings import EtlSettings

LOG_FORMAT: str = (
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


class EtlLoggingConfigurator:
    def __init__(self, settings: EtlSettings) -> None:
        self._settings = settings

    def do_configure_logging(self) -> None:
        log_level_name = self._settings.get_log_level()
        log_level = logging.getLevelName(log_level_name.upper())
        logging.basicConfig(level=log_level, format=LOG_FORMAT)

