from app.csv_utils import read_csv_data
import io
from unittest.mock import patch


def test_read_csv_data():
    csv_data = "TIME_PERIOD,OBS_VALUE\n2026-01,3.12\n2026-02,3.25\n"
    with patch("builtins.open", return_value=io.StringIO(csv_data)):
        results = list(read_csv_data("dummy.csv"))
        assert results == [(2026, 1, 3.12), (2026, 2, 3.25)]
