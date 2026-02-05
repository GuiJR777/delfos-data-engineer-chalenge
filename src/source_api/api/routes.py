# Rotas da Source API.

from typing import Any

from fastapi import APIRouter, Depends

from source_api.api.dependencies import get_signal_data_row_serializer
from source_api.api.dependencies import get_signal_name_parser
from source_api.api.dependencies import get_use_case
from source_api.api.schemas import DataQueryParameters
from source_api.api.serializers import SignalDataRowSerializer
from source_api.api.parsers import SignalNameParser
from source_api.application.models import DataQuery
from source_api.application.use_cases import GetDataUseCase

HEALTH_TAG_NAME: str = "health"
DATA_TAG_NAME: str = "data"

HEALTH_SUMMARY: str = "Health check"
HEALTH_DESCRIPTION: str = "Verifica se a API esta respondendo."

DATA_SUMMARY: str = "Consulta dados"
DATA_DESCRIPTION: str = (
    "Consulta dados do banco fonte por intervalo e sinais."
)

router = APIRouter()


@router.get(
    "/health",
    tags=[HEALTH_TAG_NAME],
    summary=HEALTH_SUMMARY,
    description=HEALTH_DESCRIPTION,
)
def get_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/data",
    tags=[DATA_TAG_NAME],
    summary=DATA_SUMMARY,
    description=DATA_DESCRIPTION,
)
def get_data(
    parameters: DataQueryParameters = Depends(),
    signal_name_parser: SignalNameParser = Depends(
        get_signal_name_parser,
    ),
    data_row_serializer: SignalDataRowSerializer = Depends(
        get_signal_data_row_serializer,
    ),
    use_case: GetDataUseCase = Depends(get_use_case),
) -> list[dict[str, Any]]:
    normalized_signal_names = (
        signal_name_parser.get_normalized_signal_names(
            parameters.signal_names,
        )
    )
    data_query = DataQuery(
        start_timestamp=parameters.start_timestamp,
        end_timestamp=parameters.end_timestamp,
        signal_names=normalized_signal_names,
        limit=parameters.limit,
        offset=parameters.offset,
    )
    data_rows = use_case.get_data_rows(data_query)

    return data_row_serializer.get_payloads(
        data_rows,
        normalized_signal_names,
    )
