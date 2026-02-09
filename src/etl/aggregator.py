# Agregacao de dados do ETL.

from collections.abc import Sequence
from datetime import datetime
from typing import Any

import pandas

from etl.constants import (
    AGGREGATION_FUNCTIONS,
    RESAMPLE_WINDOW_MINUTES,
    RESAMPLE_WINDOW_SUFFIX,
    SIGNAL_NAME_COLUMN_NAME,
    TIMESTAMP_COLUMN_NAME,
    VALUE_COLUMN_NAME,
)
from etl.entities import AggregatedSignalPoint


class TenMinuteAggregator:
    def __init__(
        self,
        window_minutes: int = RESAMPLE_WINDOW_MINUTES,
        aggregation_functions: Sequence[str] = AGGREGATION_FUNCTIONS,
    ) -> None:
        self._window_minutes = window_minutes
        self._aggregation_functions = tuple(aggregation_functions)

    def do_aggregate(
        self,
        data_rows: list[dict[str, Any]],
        signal_names: Sequence[str],
    ) -> list[AggregatedSignalPoint]:
        has_rows = bool(data_rows)
        if not has_rows:
            return []

        data_frame = pandas.DataFrame(data_rows)
        data_frame[TIMESTAMP_COLUMN_NAME] = pandas.to_datetime(
            data_frame[TIMESTAMP_COLUMN_NAME],
            errors="coerce",
        )
        data_frame = data_frame.dropna(
            subset=[TIMESTAMP_COLUMN_NAME],
        )
        data_frame = data_frame.set_index(TIMESTAMP_COLUMN_NAME)
        resample_window = (
            f"{self._window_minutes}{RESAMPLE_WINDOW_SUFFIX}"
        )
        aggregation_frame = data_frame[list(signal_names)].resample(
            resample_window,
        ).agg(list(self._aggregation_functions))
        aggregation_frame = aggregation_frame.dropna(how="all")
        aggregation_frame.columns = self._get_flat_columns(
            aggregation_frame.columns,
        )
        normalized_frame = aggregation_frame.reset_index()
        melted_frame = normalized_frame.melt(
            id_vars=[TIMESTAMP_COLUMN_NAME],
            var_name=SIGNAL_NAME_COLUMN_NAME,
            value_name=VALUE_COLUMN_NAME,
        )
        melted_frame = melted_frame.dropna(
            subset=[VALUE_COLUMN_NAME],
        )
        return self._get_aggregated_points(melted_frame)

    def _get_flat_columns(
        self,
        multi_columns: pandas.Index,
    ) -> list[str]:
        return [
            f"{column_name}_{aggregation_name}"
            for column_name, aggregation_name in multi_columns
        ]

    def _get_aggregated_points(
        self,
        data_frame: pandas.DataFrame,
    ) -> list[AggregatedSignalPoint]:
        aggregated_points: list[AggregatedSignalPoint] = []
        for _, row in data_frame.iterrows():
            timestamp_value = row[TIMESTAMP_COLUMN_NAME]
            signal_name = row[SIGNAL_NAME_COLUMN_NAME]
            value = row[VALUE_COLUMN_NAME]
            aggregated_points.append(
                AggregatedSignalPoint(
                    timestamp=self._normalize_timestamp(timestamp_value),
                    signal_name=str(signal_name),
                    value=float(value),
                )
            )
        return aggregated_points

    def _normalize_timestamp(self, timestamp_value: Any) -> datetime:
        if isinstance(timestamp_value, datetime):
            return timestamp_value

        return pandas.Timestamp(timestamp_value).to_pydatetime()
