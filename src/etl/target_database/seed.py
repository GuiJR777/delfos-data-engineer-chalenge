# Seed de sinais no banco alvo.

from collections.abc import Sequence

from sqlalchemy.dialects.postgresql import insert

from etl.target_database.constants import DEFAULT_SIGNAL_NAMES
from etl.target_database.database import TargetDatabaseSessionFactory
from etl.target_database.models import SignalModel


class TargetDatabaseSignalSeeder:
    def __init__(
        self,
        session_factory: TargetDatabaseSessionFactory,
        signal_names: Sequence[str] | None = None,
    ) -> None:
        self._session_factory = session_factory
        if signal_names is None:
            self._signal_names = tuple(DEFAULT_SIGNAL_NAMES)
            return

        self._signal_names = tuple(signal_names)

    def get_signal_names(self) -> tuple[str, ...]:
        return self._signal_names

    def do_seed_signals(self) -> None:
        signal_names = self.get_signal_names()
        has_signal_names = bool(signal_names)
        if not has_signal_names:
            return

        session = self._session_factory.get_session()
        try:
            rows = [
                {"name": signal_name}
                for signal_name in signal_names
            ]
            insert_statement = insert(SignalModel).values(rows)
            conflict_statement = (
                insert_statement.on_conflict_do_nothing(
                    index_elements=[SignalModel.name],
                )
            )
            session.execute(conflict_statement)
            session.commit()
        finally:
            session.close()

