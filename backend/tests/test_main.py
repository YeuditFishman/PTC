from app.main import app
from app.models import ExchangeRate
from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.SessionLocal")
def test_get_rates_returns_data(mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    mock_db.query().order_by().all.return_value = [
        ExchangeRate(year=2026, month=1, average_rate=3.12),
        ExchangeRate(year=2026, month=2, average_rate=3.25),
    ]

    response = client.get("/api/rates")
    assert response.status_code == 200
    assert response.json() == [
        {"year": 2026, "month": 1, "average_rate": 3.12},
        {"year": 2026, "month": 2, "average_rate": 3.25},
    ]

    mock_db.close.assert_called_once()


@patch("app.main.Base.metadata.create_all")
@patch("app.main.time.sleep", return_value=None)
def test_startup_event_runs(mock_sleep, mock_create_all):
    from app.main import startup_event

    startup_event()
    mock_create_all.assert_called_once()
    mock_sleep.assert_not_called()


@patch("app.main.Base.metadata.create_all")
@patch("app.main.time.sleep", return_value=None)
def test_startup_event_retries_then_fails(mock_sleep, mock_create_all):
    from app.main import startup_event

    mock_create_all.side_effect = Exception("DB down")

    with pytest.raises(RuntimeError) as exc_info:
        startup_event()

    assert str(exc_info.value) == "Database is not available"
    assert mock_create_all.call_count == 5
    assert mock_sleep.call_count == 5
