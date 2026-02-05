# Casos de uso da camada de aplicacao.

from source_api.application.models import DataQuery
from source_api.application.validators import DataQueryValidator
from source_api.domain.entities import SignalDataRow
from source_api.domain.ports import SourceDataRepositoryPort


class GetDataUseCase:
    def __init__(
        self,
        repository: SourceDataRepositoryPort,
        validator: DataQueryValidator,
    ) -> None:
        self._repository = repository
        self._validator = validator

    def get_data_rows(self, data_query: DataQuery) -> list[SignalDataRow]:
        self._validator.do_validate(data_query)
        return self._repository.get_data_rows(
            data_query.start_timestamp,
            data_query.end_timestamp,
            data_query.signal_names,
            data_query.limit,
            data_query.offset,
        )

