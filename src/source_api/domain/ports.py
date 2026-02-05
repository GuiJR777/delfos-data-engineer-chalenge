# Portas do dominio da Source API.

from abc import ABC, abstractmethod
from datetime import datetime

from source_api.domain.entities import SignalDataRow


class SourceDataRepositoryPort(ABC):
    @abstractmethod
    def get_data_rows(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime,
        signal_names: list[str],
        limit: int,
        offset: int,
    ) -> list[SignalDataRow]:
        raise NotImplementedError

