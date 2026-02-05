# Esquemas de entrada da API.

from datetime import datetime

from fastapi import Query

from source_api.api.constants import DEFAULT_LIMIT
from source_api.api.constants import DEFAULT_OFFSET
from source_api.api.constants import MAX_LIMIT
from source_api.api.constants import MIN_LIMIT

START_EXAMPLE: str = "2024-01-01T00:00:00"
END_EXAMPLE: str = "2024-01-01T01:00:00"
SIGNALS_EXAMPLE: list[str] = ["wind_speed", "power"]
LIMIT_EXAMPLE: int = 1000
OFFSET_EXAMPLE: int = 0


class DataQueryParameters:
    def __init__(
        self,
        start: datetime = Query(
            ...,
            description="Start datetime in ISO format",
            example=START_EXAMPLE,
        ),
        end: datetime = Query(
            ...,
            description="End datetime in ISO format",
            example=END_EXAMPLE,
        ),
        signals: list[str] = Query(
            ...,
            description="Signal names to return",
            example=SIGNALS_EXAMPLE,
        ),
        limit: int = Query(
            DEFAULT_LIMIT,
            ge=MIN_LIMIT,
            le=MAX_LIMIT,
            example=LIMIT_EXAMPLE,
        ),
        offset: int = Query(
            DEFAULT_OFFSET,
            ge=DEFAULT_OFFSET,
            example=OFFSET_EXAMPLE,
        ),
    ) -> None:
        self.start_timestamp = start
        self.end_timestamp = end
        self.signal_names = signals
        self.limit = limit
        self.offset = offset

