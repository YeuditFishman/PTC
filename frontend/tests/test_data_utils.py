from app.data_utils import compute_diff_matrix, fetch_data, forecast_next_month, multiply_matrices
import os
import pandas as pd
from unittest.mock import patch, MagicMock


def test_compute_diff_matrix():
    df = pd.DataFrame({
        "year": [2026, 2026, 2026, 2026],
        "month": [1, 2, 3, 4],
        "average_rate": [3.0, 3.2, 3.1, 3.3]
    })
    diff_matrix = compute_diff_matrix(df)
    assert diff_matrix.shape[1] == 4
    assert 'Avg' in diff_matrix.index
    assert pd.api.types.is_numeric_dtype(diff_matrix.values)


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


def test_multiply_matrices():
    df = pd.DataFrame({
        "year": [2026, 2026, 2026, 2026],
        "month": [1, 2, 3, 4],
        "average_rate": [3.0, 3.2, 3.1, 3.3]
    })
    product = multiply_matrices(df)
    assert not product.empty
    assert product.shape[1] == 4
