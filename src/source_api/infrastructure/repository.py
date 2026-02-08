# Repositorio SQLAlchemy para consultar dados da fonte.

from datetime import datetime
from typing import Any, Mapping

from sqlalchemy import text
from sqlalchemy.engine import Engine

from source_api.domain.entities import SignalDataRow
from source_api.domain.ports import SourceDataRepositoryPort

DATA_TABLE_NAME: str = "data"
TIMESTAMP_COLUMN_NAME: str = "timestamp"


class SqlAlchemySourceDataRepository(SourceDataRepositoryPort):
    def __init__(self, database_engine: Engine) -> None:
        self._database_engine = database_engine

    def get_data_rows(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime,
        signal_names: list[str],
        limit: int,
        offset: int,
    ) -> list[SignalDataRow]:
        select_columns = [TIMESTAMP_COLUMN_NAME] + list(signal_names)
        select_columns_expression = ", ".join(select_columns)
        query_text = (
            f"SELECT {select_columns_expression} "
            f"FROM {DATA_TABLE_NAME} "
            f"WHERE {TIMESTAMP_COLUMN_NAME} >= :start_timestamp "
            f"AND {TIMESTAMP_COLUMN_NAME} < :end_timestamp "
            f"ORDER BY {TIMESTAMP_COLUMN_NAME} ASC "
            "LIMIT :limit OFFSET :offset"
        )
        query = text(query_text)
        parameters = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "limit": limit,
            "offset": offset,
        }

        with self._database_engine.connect() as connection:
            result = connection.execute(query, parameters)
            rows = result.mappings().all()

        return [
            self._build_signal_data_row(row, signal_names)
            for row in rows
        ]

    def _build_signal_data_row(
        self,
        row: Mapping[str, Any],
        signal_names: list[str],
    ) -> SignalDataRow:
        timestamp = row[TIMESTAMP_COLUMN_NAME]
        signal_values = {
            signal_name: row[signal_name]
            for signal_name in signal_names
        }
        return SignalDataRow(
            timestamp=timestamp,
            signal_values=signal_values,
        )

