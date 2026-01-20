from app.data_utils import fetch_data, forecast_next_month
import os
import pandas as pd
from unittest.mock import patch, MagicMock


def test_forecast_next_month():
    df = pd.DataFrame({
        'year': [2026, 2026, 2026],
        'month': [1, 2, 3],
        'average_rate': [3.1, 3.2, 3.3]
    })
    year, month, forecast = forecast_next_month(df)
    assert year == 2026
    assert month == 4
    assert round(forecast, 2) == 3.2


@patch.dict(os.environ, {"BACKEND_URL": "http://fake-url"})
@patch("app.data_utils.requests.get")
def test_fetch_data(mock_get):
    mock_get.return_value.json.return_value = [
        {"year": 2026, "month": 1, "average_rate": 3.1},
        {"year": 2026, "month": 2, "average_rate": 3.2},
    ]
    mock_get.return_value.raise_for_status = MagicMock()
    df = fetch_data()
    assert len(df) == 2
    assert "year_month" in df.columns
