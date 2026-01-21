from app.update_exchange import update_latest_month
from unittest.mock import MagicMock


def test_update_latest_month(mock_db, mocker):
    mock_last_entry = MagicMock()
    mock_last_entry.year = 2026
    mock_last_entry.month = 1
    mock_db.query().order_by().first.return_value = mock_last_entry
    mock_db.query().filter_by().first.return_value = None
    mocker.patch("app.update_exchange.fetch_latest_rate", return_value=3.25)

    update_latest_month(mock_db)

    added_obj = mock_db.add.call_args[0][0]
    assert added_obj.year == 2026
    assert added_obj.month == 2
    assert added_obj.average_rate == 3.25
    mock_db.commit.assert_called_once()
