# Ponto de entrada da Source API.

from fastapi import FastAPI

from source_api.api.exception_handlers import (
    handle_data_query_validation_error,
)
from source_api.api.dependencies import DependencyProvider
from source_api.api.dependencies import configure_dependencies
from source_api.api.lifecycle import ApplicationLifecycle
from source_api.api.routes import router
from source_api.application.exceptions import DataQueryValidationError
from source_api.infrastructure.database import DatabaseEngineManager
from source_api.infrastructure.settings import ApplicationSettings

APPLICATION_TITLE: str = "Source API"
APPLICATION_VERSION: str = "0.1.0"
APPLICATION_DESCRIPTION: str = (
    "API para consultar dados do banco fonte. "
    "Expondo endpoints de saude e consulta de sinais."
)

OPENAPI_TAGS: list[dict[str, str]] = [
    {
        "name": "health",
        "description": "Verifica status basico da API.",
    },
    {
        "name": "data",
        "description": "Consulta dados do banco fonte.",
    },
]


application_settings = ApplicationSettings()
database_engine_manager = DatabaseEngineManager(application_settings)

dependency_provider = DependencyProvider(database_engine_manager)
configure_dependencies(dependency_provider)

lifecycle = ApplicationLifecycle(database_engine_manager)

application = FastAPI(
    title=APPLICATION_TITLE,
    version=APPLICATION_VERSION,
    description=APPLICATION_DESCRIPTION,
    openapi_tags=OPENAPI_TAGS,
)

application.include_router(router)
application.add_exception_handler(
    DataQueryValidationError,
    handle_data_query_validation_error,
)
application.add_event_handler("startup", lifecycle.do_startup)
application.add_event_handler("shutdown", lifecycle.do_shutdown)
