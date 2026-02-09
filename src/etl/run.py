# Execucao do ETL diario.

import argparse
from datetime import date
import logging
from time import perf_counter

from etl.aggregator import TenMinuteAggregator
from etl.constants import DATE_FORMAT, SOURCE_SIGNAL_NAMES
from etl.date_range import EtlDateRangeCalculator
from etl.loader import TargetDatabaseLoader
from etl.logging_config import EtlLoggingConfigurator
from etl.settings import EtlSettings
from etl.source_api_client import SourceApiClient
from etl.target_database.bootstrap import TargetDatabaseBootstrapper
from etl.target_database.database import (
    TargetDatabaseEngineManager,
    TargetDatabaseSessionFactory,
)
from etl.target_database.schema import TargetDatabaseSchemaManager
from etl.target_database.seed import TargetDatabaseSignalSeeder
from etl.target_database.settings import TargetDatabaseSettings

LOGGER = logging.getLogger(__name__)

INVALID_DATE_MESSAGE: str = "Invalid date format"
TOTAL_LOG_MESSAGE: str = "ETL completed for %s in %.2f seconds"


class EtlArgumentParser:
    def get_target_date(self) -> date:
        parser = argparse.ArgumentParser(description="Run daily ETL")
        parser.add_argument(
            "--date",
            required=True,
            help=f"Target date in format {DATE_FORMAT}",
        )
        arguments = parser.parse_args()
        return self._parse_date(arguments.date)

    def _parse_date(self, date_value: str) -> date:
        try:
            return date.fromisoformat(date_value)
        except ValueError as error:
            raise ValueError(
                f"{INVALID_DATE_MESSAGE}: {date_value}"
            ) from error


class EtlRunner:
    def __init__(
        self,
        api_client: SourceApiClient,
        date_range_calculator: EtlDateRangeCalculator,
        aggregator: TenMinuteAggregator,
        loader: TargetDatabaseLoader,
        bootstrapper: TargetDatabaseBootstrapper,
        engine_manager: TargetDatabaseEngineManager,
    ) -> None:
        self._api_client = api_client
        self._date_range_calculator = date_range_calculator
        self._aggregator = aggregator
        self._loader = loader
        self._bootstrapper = bootstrapper
        self._engine_manager = engine_manager

    def do_run(self, target_date: date) -> int:
        total_start = perf_counter()
        try:
            self._engine_manager.do_startup()
            self._bootstrapper.do_bootstrap()
            date_range = self._date_range_calculator.get_date_range(
                target_date
            )
            extract_start = perf_counter()
            data_rows = self._api_client.do_fetch_data(
                start_timestamp=date_range.start.isoformat(),
                end_timestamp=date_range.end.isoformat(),
                signal_names=SOURCE_SIGNAL_NAMES,
            )
            extract_seconds = perf_counter() - extract_start
            LOGGER.info(
                "Extracted %s rows in %.2f seconds",
                len(data_rows),
                extract_seconds,
            )

            transform_start = perf_counter()
            aggregated_points = self._aggregator.do_aggregate(
                data_rows=data_rows,
                signal_names=SOURCE_SIGNAL_NAMES,
            )
            transform_seconds = perf_counter() - transform_start
            LOGGER.info(
                "Aggregated %s points in %.2f seconds",
                len(aggregated_points),
                transform_seconds,
            )

            load_start = perf_counter()
            inserted_count = self._loader.do_load(
                aggregated_points=aggregated_points,
                day_start=date_range.start,
                day_end=date_range.end,
            )
            load_seconds = perf_counter() - load_start
            LOGGER.info(
                "Loaded %s rows in %.2f seconds",
                inserted_count,
                load_seconds,
            )
            return inserted_count
        finally:
            total_seconds = perf_counter() - total_start
            LOGGER.info(
                TOTAL_LOG_MESSAGE,
                target_date.isoformat(),
                total_seconds,
            )
            self._api_client.do_close()
            self._engine_manager.do_shutdown()


class EtlRunnerFactory:
    def __init__(self, settings: EtlSettings) -> None:
        self._settings = settings

    def get_runner(
        self,
        api_client: SourceApiClient | None = None,
        engine_manager: TargetDatabaseEngineManager | None = None,
    ) -> EtlRunner:
        target_settings = TargetDatabaseSettings()
        if engine_manager is None:
            engine_manager = TargetDatabaseEngineManager(
                target_settings
            )
        session_factory = TargetDatabaseSessionFactory(engine_manager)
        schema_manager = TargetDatabaseSchemaManager(engine_manager)
        signal_seeder = TargetDatabaseSignalSeeder(session_factory)
        bootstrapper = TargetDatabaseBootstrapper(
            schema_manager=schema_manager,
            signal_seeder=signal_seeder,
        )
        if api_client is None:
            api_client = SourceApiClient(
                base_url=self._settings.get_api_base_url(),
                timeout_seconds=self._settings.get_api_timeout_seconds(),
                retry_attempts=self._settings.get_api_retry_attempts(),
                api_limit=self._settings.get_api_limit(),
                api_offset=self._settings.get_api_offset(),
            )
        aggregator = TenMinuteAggregator()
        loader = TargetDatabaseLoader(session_factory)
        date_range_calculator = EtlDateRangeCalculator()
        return EtlRunner(
            api_client=api_client,
            date_range_calculator=date_range_calculator,
            aggregator=aggregator,
            loader=loader,
            bootstrapper=bootstrapper,
            engine_manager=engine_manager,
        )


def run_daily_etl(
    target_date: date,
    api_client: SourceApiClient | None = None,
    engine_manager: TargetDatabaseEngineManager | None = None,
    settings: EtlSettings | None = None,
) -> int:
    runtime_settings = settings or EtlSettings()
    runner_factory = EtlRunnerFactory(runtime_settings)
    runner = runner_factory.get_runner(
        api_client=api_client,
        engine_manager=engine_manager,
    )
    return runner.do_run(target_date)


def main() -> None:
    settings = EtlSettings()
    logging_configurator = EtlLoggingConfigurator(settings)
    logging_configurator.do_configure_logging()
    argument_parser = EtlArgumentParser()
    target_date = argument_parser.get_target_date()
    run_daily_etl(
        target_date=target_date,
        settings=settings,
    )


if __name__ == "__main__":
    main()
