# Entidades do ETL.

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AggregatedSignalPoint:
    timestamp: datetime
    signal_name: str
    value: float

