import sys
from datetime import date as real_date, datetime
from unittest.mock import MagicMock

import pytest

from scripts import seed_source_db


class FakeDate:
    @classmethod
    def today(cls):
        return real_date(2024, 1, 10)


def build_connection_mocks():
    cursor_one = MagicMock()
    cursor_two = MagicMock()

    cursor_cm_one = MagicMock()
    cursor_cm_one.__enter__.return_value = cursor_one

    cursor_cm_two = MagicMock()
    cursor_cm_two.__enter__.return_value = cursor_two

    conn = MagicMock()
    conn.__enter__.return_value = conn
    conn.cursor.side_effect = [cursor_cm_one, cursor_cm_two]

    return conn, cursor_one, cursor_two


class TestMain:
    def test_when_start_date_is_provided_should_insert_rows_and_write_seed_info(self, monkeypatch):
        # Arrange

        monkeypatch.setenv("SOURCE_DATABASE_URL", "postgresql+psycopg2://user:pass@localhost:5432/db")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "seed_source_db.py",
                "--start-date",
                "2024-01-01",
                "--days",
                "1",
                "--truncate",
                "--batch-size",
                "500",
                "--seed",
                "7",
                "--output",
                "out.json",
            ],
        )

        load_dotenv = MagicMock()
        build_rows = MagicMock(
            return_value=[
                (datetime(2024, 1, 1, 0, 0, 0), 1.0, 2.0, 3.0),
                (datetime(2024, 1, 1, 0, 1, 0), 1.1, 2.1, 3.1),
            ]
        )
        write_seed_info = MagicMock()
        execute_values = MagicMock()

        monkeypatch.setattr(seed_source_db, "load_dotenv", load_dotenv)
        monkeypatch.setattr(seed_source_db, "build_rows", build_rows)
        monkeypatch.setattr(seed_source_db, "write_seed_info", write_seed_info)
        monkeypatch.setattr(seed_source_db, "execute_values", execute_values)

        conn, cursor_one, cursor_two = build_connection_mocks()
        connect = MagicMock(return_value=conn)
        monkeypatch.setattr(seed_source_db.psycopg2, "connect", connect)

        # Act

        seed_source_db.main()

        # Assert

        connect.assert_called_once_with("postgresql://user:pass@localhost:5432/db")
        cursor_one.execute.assert_any_call("TRUNCATE TABLE data;")
        execute_values.assert_called_once()
        write_seed_info.assert_called_once_with(
            "out.json",
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 2, 0, 0, 0),
            2,
        )
        build_rows.assert_called_once_with(
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 2, 0, 0, 0),
            7,
        )

        execute_args = execute_values.call_args
        assert execute_args.args[0] is cursor_two
        assert (
            execute_args.args[1]
            == "INSERT INTO data (timestamp, wind_speed, power, ambient_temperature) VALUES %s"
        )
        assert execute_args.args[2] == build_rows.return_value
        assert execute_args.kwargs["page_size"] == 500

    def test_when_database_url_is_missing_should_raise_system_exit(self, monkeypatch):
        # Arrange

        monkeypatch.delenv("SOURCE_DATABASE_URL", raising=False)
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.setattr(sys, "argv", ["seed_source_db.py", "--start-date", "2024-01-01"])
        monkeypatch.setattr(seed_source_db, "load_dotenv", MagicMock())

        # Act

        with pytest.raises(SystemExit) as excinfo:
            seed_source_db.main()

        # Assert

        assert str(excinfo.value) == "SOURCE_DATABASE_URL is not set"

    def test_when_start_date_is_not_provided_should_use_today_minus_days(self, monkeypatch):
        # Arrange

        monkeypatch.setenv("SEED_DAYS", "2")
        monkeypatch.setenv("SOURCE_DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
        monkeypatch.setattr(sys, "argv", ["seed_source_db.py"])
        monkeypatch.setattr(seed_source_db, "load_dotenv", MagicMock())
        monkeypatch.setattr(seed_source_db, "date", FakeDate)

        build_rows = MagicMock(
            return_value=[
                (datetime(2024, 1, 8, 0, 0, 0), 1.0, 2.0, 3.0),
                (datetime(2024, 1, 8, 0, 1, 0), 1.1, 2.1, 3.1),
            ]
        )

        monkeypatch.setattr(seed_source_db, "build_rows", build_rows)
        monkeypatch.setattr(seed_source_db, "write_seed_info", MagicMock())
        monkeypatch.setattr(seed_source_db, "execute_values", MagicMock())

        conn, _, _ = build_connection_mocks()
        connect = MagicMock(return_value=conn)
        monkeypatch.setattr(seed_source_db.psycopg2, "connect", connect)

        # Act

        seed_source_db.main()

        # Assert

        build_rows.assert_called_once_with(
            datetime(2024, 1, 8, 0, 0, 0),
            datetime(2024, 1, 10, 0, 0, 0),
            42,
        )
