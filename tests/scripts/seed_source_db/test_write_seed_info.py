import json
from datetime import datetime

from scripts import seed_source_db


class TestWriteSeedInfo:
    def test_when_called_should_write_seed_metadata(self, tmp_path):
        # Arrange

        path = tmp_path / "seed_info.json"
        start_ts = datetime(2024, 1, 1, 0, 0, 0)
        end_ts = datetime(2024, 1, 2, 0, 0, 0)

        # Act

        seed_source_db.write_seed_info(str(path), start_ts, end_ts, rows=10)

        # Assert

        payload = json.loads(path.read_text())
        assert payload["start_ts"] == start_ts.isoformat()
        assert payload["end_ts"] == end_ts.isoformat()
        assert payload["rows"] == 10
        assert payload["frequency_minutes"] == 1
        assert payload["generated_at"].endswith("Z")
