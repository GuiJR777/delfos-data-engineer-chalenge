# Tests for EtlLoggingConfigurator.

from unittest.mock import MagicMock

import etl.logging_config as logging_module
from etl.logging_config import EtlLoggingConfigurator


class TestDoConfigureLogging:
    def test_when_called_should_configure_logging(self, monkeypatch):
        # Arrange

        settings = MagicMock()
        settings.get_log_level.return_value = "INFO"

        get_level_name = MagicMock(return_value="INFO")
        basic_config = MagicMock()

        monkeypatch.setattr(logging_module.logging, "getLevelName", get_level_name)
        monkeypatch.setattr(logging_module.logging, "basicConfig", basic_config)

        configurator = EtlLoggingConfigurator(settings)

        # Act

        configurator.do_configure_logging()

        # Assert

        get_level_name.assert_called_once_with("INFO")
        basic_config.assert_called_once_with(
            level="INFO",
            format=logging_module.LOG_FORMAT,
        )
