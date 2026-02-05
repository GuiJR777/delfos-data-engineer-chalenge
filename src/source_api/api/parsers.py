# Parsers da camada de API.

from source_api.api.constants import SIGNAL_SEPARATOR
from source_api.api.constants import ZERO_COUNT


class SignalNameParser:
    def get_normalized_signal_names(
        self,
        signal_names: list[str],
    ) -> list[str]:
        has_signal_names = len(signal_names) > ZERO_COUNT
        if not has_signal_names:
            return []

        expanded_signal_names = self._get_expanded_signal_names(signal_names)
        stripped_signal_names = [
            signal_name.strip() for signal_name in expanded_signal_names
        ]
        normalized_signal_names = [
            signal_name
            for signal_name in stripped_signal_names
            if signal_name
        ]

        return normalized_signal_names

    def _get_expanded_signal_names(
        self,
        signal_names: list[str],
    ) -> list[str]:
        has_separator = any(
            SIGNAL_SEPARATOR in signal_name for signal_name in signal_names
        )
        if not has_separator:
            return list(signal_names)

        expanded_signal_names: list[str] = []
        for signal_name in signal_names:
            expanded_signal_names.extend(signal_name.split(SIGNAL_SEPARATOR))

        return expanded_signal_names

