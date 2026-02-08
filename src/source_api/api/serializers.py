# Serializadores de resposta da API.

from typing import Any

from source_api.domain.entities import SignalDataRow

TIMESTAMP_FIELD_NAME: str = "timestamp"


class SignalDataRowSerializer:
    def get_payload(
        self,
        data_row: SignalDataRow,
        signal_names: list[str],
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            TIMESTAMP_FIELD_NAME: data_row.timestamp,
        }
        for signal_name in signal_names:
            payload[signal_name] = data_row.signal_values.get(signal_name)
        return payload

    def get_payloads(
        self,
        data_rows: list[SignalDataRow],
        signal_names: list[str],
    ) -> list[dict[str, Any]]:
        return [
            self.get_payload(data_row, signal_names)
            for data_row in data_rows
        ]

