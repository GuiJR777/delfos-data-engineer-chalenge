import sys

from scripts import seed_source_db


class TestParseArgs:
    def test_when_no_args_should_use_default_values(self, monkeypatch):
        # Arrange

        monkeypatch.setenv("SEED_DAYS", "7")
        monkeypatch.setattr(sys, "argv", ["seed_source_db.py"])

        # Act

        args = seed_source_db.parse_args()

        # Assert

        assert args.start_date is None
        assert args.days == 7
        assert args.truncate is False
        assert args.batch_size == 1000
        assert args.seed == 42
        assert args.output == "seed_info.json"

    def test_when_custom_args_are_provided_should_parse_values(self, monkeypatch):
        # Arrange

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "seed_source_db.py",
                "--start-date",
                "2024-01-01",
                "--days",
                "5",
                "--truncate",
                "--batch-size",
                "500",
                "--seed",
                "99",
                "--output",
                "custom.json",
            ],
        )

        # Act

        args = seed_source_db.parse_args()

        # Assert

        assert args.start_date == "2024-01-01"
        assert args.days == 5
        assert args.truncate is True
        assert args.batch_size == 500
        assert args.seed == 99
        assert args.output == "custom.json"
