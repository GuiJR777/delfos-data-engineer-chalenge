# Modelos da camada de aplicacao.

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DataQuery:
    start_timestamp: datetime
    end_timestamp: datetime
    signal_names: list[str]
    limit: int
    offset: int

