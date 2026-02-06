# Tests for main module wiring.

import importlib
from unittest.mock import MagicMock

import fastapi

import source_api.api.dependencies as dependencies_module
import source_api.api.exception_handlers as exception_handlers_module
import source_api.api.lifecycle as lifecycle_module
import source_api.api.routes as routes_module
import source_api.application.exceptions as exceptions_module
import source_api.infrastructure.database as database_module
import source_api.infrastructure.settings as settings_module


class TestMainModule:
    def test_when_module_is_loaded_should_configure_application(self, monkeypatch):
        # Arrange

        application_instance = MagicMock()
        fastapi_class = MagicMock(return_value=application_instance)
        monkeypatch.setattr(fastapi, "FastAPI", fastapi_class)

        settings_instance = MagicMock()
        settings_class = MagicMock(return_value=settings_instance)
        monkeypatch.setattr(
            settings_module,
            "ApplicationSettings",
            settings_class,
        )

        manager_instance = MagicMock()
        manager_class = MagicMock(return_value=manager_instance)
        monkeypatch.setattr(
            database_module,
            "DatabaseEngineManager",
            manager_class,
        )

        provider_instance = MagicMock()
        provider_class = MagicMock(return_value=provider_instance)
        monkeypatch.setattr(
            dependencies_module,
            "DependencyProvider",
            provider_class,
        )

        configure_dependencies = MagicMock()
        monkeypatch.setattr(
            dependencies_module,
            "configure_dependencies",
            configure_dependencies,
        )

        lifecycle_instance = MagicMock()
        lifecycle_class = MagicMock(return_value=lifecycle_instance)
        monkeypatch.setattr(
            lifecycle_module,
            "ApplicationLifecycle",
            lifecycle_class,
        )

        router = MagicMock()
        monkeypatch.setattr(routes_module, "router", router)

        handler = MagicMock()
        monkeypatch.setattr(
            exception_handlers_module,
            "handle_data_query_validation_error",
            handler,
        )

        exception_class = MagicMock()
        monkeypatch.setattr(
            exceptions_module,
            "DataQueryValidationError",
            exception_class,
        )

        # Act

        import source_api.main as main_module
        importlib.reload(main_module)

        # Assert

        last_call = fastapi_class.call_args_list[-1]
        expected_kwargs = {
            "title": main_module.APPLICATION_TITLE,
            "version": main_module.APPLICATION_VERSION,
            "description": main_module.APPLICATION_DESCRIPTION,
            "openapi_tags": main_module.OPENAPI_TAGS,
        }

        fastapi_class.assert_called_with(
            title=main_module.APPLICATION_TITLE,
            version=main_module.APPLICATION_VERSION,
            description=main_module.APPLICATION_DESCRIPTION,
            openapi_tags=main_module.OPENAPI_TAGS,
        )
        assert last_call.kwargs == expected_kwargs
        configure_dependencies.assert_any_call(provider_instance)
        assert configure_dependencies.call_count >= 1
        application_instance.include_router.assert_any_call(router)
        assert application_instance.include_router.call_count >= 1
        application_instance.add_exception_handler.assert_any_call(
            exception_class,
            handler,
        )
        assert application_instance.add_exception_handler.call_count >= 1
        application_instance.add_event_handler.assert_any_call(
            "startup",
            lifecycle_instance.do_startup,
        )
        application_instance.add_event_handler.assert_any_call(
            "shutdown",
            lifecycle_instance.do_shutdown,
        )

