# Tests for TargetDatabaseLoader.

from datetime import datetime
from unittest.mock import MagicMock

import pytest

import etl.loader as loader_module
from etl.entities import AggregatedSignalPoint
from etl.loader import TargetDatabaseLoader


class TestDoLoad:
    def test_when_no_points_should_return_zero(self):
        # Arrange

        session_factory = MagicMock()
        loader = TargetDatabaseLoader(session_factory)

        # Act

        result = loader.do_load(
            aggregated_points=[],
            day_start=datetime(2024, 1, 1, 0, 0, 0),
            day_end=datetime(2024, 1, 2, 0, 0, 0),
        )

        # Assert

        assert result == 0
        session_factory.get_session.assert_not_called()

    def test_when_points_are_present_should_commit(self, monkeypatch):
        # Arrange

        session = MagicMock()
        session_factory = MagicMock()
        session_factory.get_session.return_value = session

        loader = TargetDatabaseLoader(session_factory)
        loader._get_signal_id_mapping = MagicMock(
            return_value={"wind_speed_mean": 1}
        )
        loader._do_delete_existing = MagicMock()
        loader._do_insert_batches = MagicMock(return_value=5)

        points = [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.0,
            )
        ]

        # Act

        result = loader.do_load(
            aggregated_points=points,
            day_start=datetime(2024, 1, 1, 0, 0, 0),
            day_end=datetime(2024, 1, 2, 0, 0, 0),
        )

        # Assert

        assert result == 5
        session.commit.assert_called_once_with()
        session.close.assert_called_once_with()

    def test_when_called_twice_should_delete_each_time(self):
        # Arrange

        session = MagicMock()
        session_factory = MagicMock()
        session_factory.get_session.return_value = session

        loader = TargetDatabaseLoader(session_factory)
        loader._get_signal_id_mapping = MagicMock(
            return_value={"wind_speed_mean": 1}
        )
        loader._do_delete_existing = MagicMock()
        loader._do_insert_batches = MagicMock(return_value=1)

        points = [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.0,
            )
        ]
        day_start = datetime(2024, 1, 1, 0, 0, 0)
        day_end = datetime(2024, 1, 2, 0, 0, 0)

        # Act

        loader.do_load(
            aggregated_points=points,
            day_start=day_start,
            day_end=day_end,
        )
        loader.do_load(
            aggregated_points=points,
            day_start=day_start,
            day_end=day_end,
        )

        # Assert

        assert loader._do_delete_existing.call_count == 2
        loader._do_delete_existing.assert_any_call(
            session,
            day_start,
            day_end,
            (1,),
        )
        assert loader._do_insert_batches.call_count == 2

class TestGetSignalIdMapping:
    def test_when_all_signals_exist_should_return_mapping(self):
        # Arrange

        session = MagicMock()
        signal_one = MagicMock()
        signal_one.name = "wind_speed_mean"
        signal_one.id = 1
        signal_two = MagicMock()
        signal_two.name = "power_mean"
        signal_two.id = 2

        session.execute.return_value.scalars.return_value.all.return_value = [
            signal_one,
            signal_two,
        ]

        loader = TargetDatabaseLoader(MagicMock())
        points = [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.0,
            ),
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="power_mean",
                value=2.0,
            ),
        ]

        # Act

        result = loader._get_signal_id_mapping(session, points)

        # Assert

        assert result == {"wind_speed_mean": 1, "power_mean": 2}

    def test_when_signal_is_missing_should_raise_error(self):
        # Arrange

        session = MagicMock()
        signal_one = MagicMock()
        signal_one.name = "wind_speed_mean"
        signal_one.id = 1

        session.execute.return_value.scalars.return_value.all.return_value = [
            signal_one
        ]

        loader = TargetDatabaseLoader(MagicMock())
        points = [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.0,
            ),
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="power_mean",
                value=2.0,
            ),
        ]

        # Act

        with pytest.raises(RuntimeError):
            loader._get_signal_id_mapping(session, points)

        # Assert


class TestDoDeleteExisting:
    def test_when_called_should_execute_delete(self):
        # Arrange

        session = MagicMock()
        loader = TargetDatabaseLoader(MagicMock())

        # Act

        loader._do_delete_existing(
            session=session,
            day_start=datetime(2024, 1, 1, 0, 0, 0),
            day_end=datetime(2024, 1, 2, 0, 0, 0),
            signal_ids=(1, 2),
        )

        # Assert

        session.execute.assert_called_once()


class TestDoInsertBatches:
    def test_when_rows_exceed_batch_size_should_insert_multiple(self, monkeypatch):
        # Arrange

        session = MagicMock()
        loader = TargetDatabaseLoader(MagicMock(), batch_size=2)
        loader._get_rows = MagicMock(
            return_value=[
                {"timestamp": 1, "signal_id": 1, "value": 1.0},
                {"timestamp": 2, "signal_id": 1, "value": 2.0},
                {"timestamp": 3, "signal_id": 1, "value": 3.0},
            ]
        )

        insert_statement = MagicMock()
        insert_statement.on_conflict_do_nothing.return_value = MagicMock()
        insert_mock = MagicMock(return_value=insert_statement)
        monkeypatch.setattr(loader_module, "insert", insert_mock)

        # Act

        result = loader._do_insert_batches(
            session=session,
            aggregated_points=[],
            signal_id_mapping={},
        )

        # Assert

        assert result == 3
        assert session.execute.call_count == 2


class TestGetRows:
    def test_when_points_are_provided_should_build_rows(self):
        # Arrange

        loader = TargetDatabaseLoader(MagicMock())
        points = [
            AggregatedSignalPoint(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                signal_name="wind_speed_mean",
                value=1.0,
            )
        ]
        mapping = {"wind_speed_mean": 10}

        # Act

        result = loader._get_rows(points, mapping)

        # Assert

        assert result == [
            {
                "timestamp": datetime(2024, 1, 1, 0, 0, 0),
                "signal_id": 10,
                "value": 1.0,
            }
        ]

