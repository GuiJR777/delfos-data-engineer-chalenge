# Entidades do dominio da Source API.

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SignalDataRow:
    timestamp: datetime
    signal_values: dict[str, float | None]

