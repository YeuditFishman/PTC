from app.database import get_db
from app.main import app
from app.models import ExchangeRate
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

client = TestClient(app)


def test_get_rates_returns_data():
    mock_db = MagicMock()
    mock_db.query().order_by().all.return_value = [
        ExchangeRate(year=2026, month=1, average_rate=3.12)
    ]

    def override_get_db():
        try:
            yield mock_db
        finally:
            mock_db.close()

    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/api/rates")
    assert response.status_code == 200
    assert response.json() == [
        {
            "year": 2026,
            "month": 1,
            "average_rate": 3.12
            }
        ]
    app.dependency_overrides.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
