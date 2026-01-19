from app import seed
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_session():
    with patch("app.seed.SessionLocal") as mock_session_cls:
        mock_db = MagicMock()
        mock_session_cls.return_value = mock_db
        yield mock_db


@pytest.fixture
def mock_open_csv():
    csv_content = "TIME_PERIOD,OBS_VALUE\n2026-01,3.12\n2026-02,3.25\n"
    with patch("builtins.open", new_callable=MagicMock) as mock_file:
        mock_file.return_value.__enter__.return_value = (
            csv_content.splitlines()
        )
        yield mock_file


def test_seed_runs_without_error(mock_session, mock_open_csv):
    with patch("csv.DictReader") as mock_csv_reader:
        mock_csv_reader.return_value = [
            {"TIME_PERIOD": "2026-01", "OBS_VALUE": "3.12"},
            {"TIME_PERIOD": "2026-02", "OBS_VALUE": "3.25"},
        ]
        seed.Base.metadata.create_all = MagicMock()
        seed.SessionLocal = MagicMock(return_value=mock_session)
        mock_session.query().filter_by().first.return_value = None

        try:
            seed.run_seed()
        except Exception as e:
            pytest.fail(f"Seed script failed with exception: {e}")
