# Tests for DailyEtlAssetExecutor.

from unittest.mock import MagicMock

import orchestration.assets.etl_asset as asset_module
from orchestration.assets.etl_asset import DailyEtlAssetExecutor


class TestDoMaterialize:
    def test_when_called_should_run_daily_etl(self, monkeypatch):
        # Arrange

        api_client = MagicMock()
        engine_manager = MagicMock()

        executor = DailyEtlAssetExecutor(
            api_client=api_client,
            engine_manager=engine_manager,
        )

        context = MagicMock()
        context.partition_key = "2024-01-01"

        run_daily_etl = MagicMock(return_value=5)
        monkeypatch.setattr(
            asset_module,
            "run_daily_etl",
            run_daily_etl,
        )

        # Act

        result = executor.do_materialize(context)

        # Assert

        assert result == 5
        run_daily_etl.assert_called_once_with(
            target_date=executor._get_target_date("2024-01-01"),
            api_client=api_client,
            engine_manager=engine_manager,
        )


class TestGetTargetDate:
    def test_when_partition_key_is_provided_should_parse_date(self):
        # Arrange

        executor = DailyEtlAssetExecutor(
            api_client=MagicMock(),
            engine_manager=MagicMock(),
        )

        # Act

        result = executor._get_target_date("2024-01-01")

        # Assert

        assert result.isoformat() == "2024-01-01"

