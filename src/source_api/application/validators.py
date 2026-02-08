# Validacoes da camada de aplicacao.

from typing import Iterable

from source_api.application.exceptions import DataQueryValidationError
from source_api.application.models import DataQuery

ZERO_COUNT: int = 0

START_END_INVALID_MESSAGE: str = "start must be before end"
SIGNALS_EMPTY_MESSAGE: str = "signals must contain at least one entry"
INVALID_SIGNALS_MESSAGE_PREFIX: str = (
    "Invalid signals requested. Allowed signals: "
)
INVALID_SIGNALS_MESSAGE_SUFFIX: str = "."


class DataQueryValidator:
    def __init__(self, allowed_signal_names: Iterable[str]) -> None:
        self._allowed_signal_names = set(allowed_signal_names)

    def do_validate(self, data_query: DataQuery) -> None:
        is_interval_valid = (
            data_query.start_timestamp < data_query.end_timestamp
        )
        if not is_interval_valid:
            raise DataQueryValidationError(START_END_INVALID_MESSAGE)

        has_signal_names = len(data_query.signal_names) > ZERO_COUNT
        if not has_signal_names:
            raise DataQueryValidationError(SIGNALS_EMPTY_MESSAGE)

        invalid_signal_names = self.get_invalid_signal_names(
            data_query.signal_names,
        )
        has_invalid_signal_names = len(invalid_signal_names) > ZERO_COUNT
        if not has_invalid_signal_names:
            return

        allowed_signal_names = sorted(self._allowed_signal_names)
        allowed_signal_names_message = ", ".join(allowed_signal_names)
        detail_message = (
            INVALID_SIGNALS_MESSAGE_PREFIX
            + allowed_signal_names_message
            + INVALID_SIGNALS_MESSAGE_SUFFIX
        )
        raise DataQueryValidationError(detail_message)

    def get_invalid_signal_names(
        self,
        signal_names: list[str],
    ) -> list[str]:
        invalid_signal_names = [
            signal_name
            for signal_name in signal_names
            if signal_name not in self._allowed_signal_names
        ]
        return invalid_signal_names

