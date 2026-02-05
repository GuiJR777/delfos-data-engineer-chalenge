# Dependencias da camada de API.

from fastapi import HTTPException, status

from source_api.api.parsers import SignalNameParser
from source_api.api.serializers import SignalDataRowSerializer
from source_api.application.constants import ALLOWED_SIGNAL_NAMES
from source_api.application.use_cases import GetDataUseCase
from source_api.application.validators import DataQueryValidator
from source_api.infrastructure.database import DatabaseEngineManager
from source_api.infrastructure.repository import SqlAlchemySourceDataRepository

HTTP_SERVICE_UNAVAILABLE: int = status.HTTP_503_SERVICE_UNAVAILABLE
DEPENDENCY_PROVIDER_NOT_CONFIGURED_MESSAGE: str = (
    "Dependency provider is not configured"
)


class DependencyProvider:
    def __init__(self, database_engine_manager: DatabaseEngineManager) -> None:
        self._database_engine_manager = database_engine_manager

    def get_signal_name_parser(self) -> SignalNameParser:
        return SignalNameParser()

    def get_signal_data_row_serializer(self) -> SignalDataRowSerializer:
        return SignalDataRowSerializer()

    def get_data_query_validator(self) -> DataQueryValidator:
        return DataQueryValidator(ALLOWED_SIGNAL_NAMES)

    def get_repository(self) -> SqlAlchemySourceDataRepository:
        has_database_engine = (
            self._database_engine_manager.is_database_engine_initialized()
        )
        if not has_database_engine:
            raise HTTPException(
                status_code=HTTP_SERVICE_UNAVAILABLE,
                detail="Database engine is not initialized",
            )

        database_engine = self._database_engine_manager.get_database_engine()
        return SqlAlchemySourceDataRepository(database_engine)

    def get_use_case(self) -> GetDataUseCase:
        repository = self.get_repository()
        validator = self.get_data_query_validator()
        return GetDataUseCase(repository, validator)


_dependency_provider: DependencyProvider | None = None


def configure_dependencies(provider: DependencyProvider) -> None:
    global _dependency_provider
    _dependency_provider = provider


def _get_dependency_provider() -> DependencyProvider:
    has_dependency_provider = _dependency_provider is not None
    if not has_dependency_provider:
        raise RuntimeError(DEPENDENCY_PROVIDER_NOT_CONFIGURED_MESSAGE)

    return _dependency_provider


def get_signal_name_parser() -> SignalNameParser:
    return _get_dependency_provider().get_signal_name_parser()


def get_signal_data_row_serializer() -> SignalDataRowSerializer:
    return _get_dependency_provider().get_signal_data_row_serializer()


def get_use_case() -> GetDataUseCase:
    return _get_dependency_provider().get_use_case()

