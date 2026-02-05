from unittest.mock import MagicMock

from scripts import seed_source_db


class TestEnsureTable:
    def test_when_called_should_execute_create_table_and_index(self):
        # Arrange

        cursor = MagicMock()

        # Act

        seed_source_db.ensure_table(cursor)

        # Assert

        create_call = cursor.execute.call_args_list[0][0][0]
        index_call = cursor.execute.call_args_list[1][0][0]
        assert "CREATE TABLE IF NOT EXISTS data" in create_call
        assert index_call == "CREATE INDEX IF NOT EXISTS idx_data_timestamp ON data (timestamp);"
