# Carga de dados agregados no banco alvo.

from collections.abc import Sequence
from datetime import datetime
import logging

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from etl.constants import DEFAULT_INSERT_BATCH_SIZE
from etl.entities import AggregatedSignalPoint
from etl.target_database.database import TargetDatabaseSessionFactory
from etl.target_database.models import DataModel, SignalModel

LOGGER = logging.getLogger(__name__)

MISSING_SIGNALS_MESSAGE: str = "Missing signals in target database"


class TargetDatabaseLoader:
    def __init__(
        self,
        session_factory: TargetDatabaseSessionFactory,
        batch_size: int = DEFAULT_INSERT_BATCH_SIZE,
    ) -> None:
        self._session_factory = session_factory
        self._batch_size = batch_size

    def do_load(
        self,
        aggregated_points: Sequence[AggregatedSignalPoint],
        day_start: datetime,
        day_end: datetime,
    ) -> int:
        has_points = bool(aggregated_points)
        if not has_points:
            return 0

        session = self._session_factory.get_session()
        try:
            signal_id_mapping = self._get_signal_id_mapping(
                session,
                aggregated_points,
            )
            self._do_delete_existing(
                session,
                day_start,
                day_end,
                tuple(signal_id_mapping.values()),
            )
            inserted_count = self._do_insert_batches(
                session,
                aggregated_points,
                signal_id_mapping,
            )
            session.commit()
            return inserted_count
        except Exception as error:
            LOGGER.exception(
                "Failed to load aggregated data: %s",
                error,
            )
            session.rollback()
            raise
        finally:
            session.close()

    def _get_signal_id_mapping(
        self,
        session: Session,
        aggregated_points: Sequence[AggregatedSignalPoint],
    ) -> dict[str, int]:
        signal_names = sorted(
            {
                point.signal_name
                for point in aggregated_points
            }
        )
        query = select(SignalModel).where(
            SignalModel.name.in_(signal_names),
        )
        results = session.execute(query).scalars().all()
        mapping = {
            signal.name: signal.id
            for signal in results
        }
        missing_names = [
            name for name in signal_names if name not in mapping
        ]
        has_missing_names = bool(missing_names)
        if has_missing_names:
            raise RuntimeError(
                f"{MISSING_SIGNALS_MESSAGE}: {missing_names}"
            )
        return mapping

    def _do_delete_existing(
        self,
        session: Session,
        day_start: datetime,
        day_end: datetime,
        signal_ids: tuple[int, ...],
    ) -> None:
        delete_statement = delete(DataModel).where(
            DataModel.timestamp >= day_start,
            DataModel.timestamp < day_end,
            DataModel.signal_id.in_(signal_ids),
        )
        session.execute(delete_statement)

    def _do_insert_batches(
        self,
        session: Session,
        aggregated_points: Sequence[AggregatedSignalPoint],
        signal_id_mapping: dict[str, int],
    ) -> int:
        rows = self._get_rows(aggregated_points, signal_id_mapping)
        total_rows = len(rows)
        inserted_rows = 0
        start_index = 0
        while start_index < total_rows:
            end_index = start_index + self._batch_size
            batch = rows[start_index:end_index]
            insert_statement = insert(DataModel).values(batch)
            conflict_statement = (
                insert_statement.on_conflict_do_nothing(
                    index_elements=[
                        DataModel.timestamp,
                        DataModel.signal_id,
                    ],
                )
            )
            session.execute(conflict_statement)
            inserted_rows = inserted_rows + len(batch)
            start_index = end_index
        return inserted_rows

    def _get_rows(
        self,
        aggregated_points: Sequence[AggregatedSignalPoint],
        signal_id_mapping: dict[str, int],
    ) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for point in aggregated_points:
            signal_id = signal_id_mapping[point.signal_name]
            rows.append(
                {
                    "timestamp": point.timestamp,
                    "signal_id": signal_id,
                    "value": point.value,
                }
            )
        return rows

