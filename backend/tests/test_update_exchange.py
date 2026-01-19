from app.models import ExchangeRate
from app.update_exchange import fetch_latest_rate, update_latest_month
from unittest.mock import patch, MagicMock


@patch("app.update_exchange.requests.get")
def test_fetch_latest_rate(mock_get):
    csv_text = "".join(
        [
            "SERIES_CODE,FREQ,BASE_CURRENCY,COUNTER_CURRENCY,"
            "UNIT_MEASURE,DATA_TYPE,DATA_SOURCE,TIME_COLLECT,"
            "CONF_STATUS,PUB_WEBSITE,UNIT_MULT,COMMENTS,"
            "TIME_PERIOD,OBS_VALUE,RELEASE_STATUS\n",
            "RER_USD_ILS,M,USD,ILS,unit,mean,source,2026-01,"
            "Confirmed,url,1,,2026-01,3.12,\n",
        ]
    )

    mock_response = MagicMock()
    mock_response.text = csv_text
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    rate = fetch_latest_rate(2026, 1)
    assert rate == 3.12


@patch("app.update_exchange.fetch_latest_rate")
@patch("app.update_exchange.SessionLocal")
def test_update_latest_month(mock_session, mock_fetch_rate):
    mock_fetch_rate.return_value = 3.25

    mock_db = MagicMock()
    mock_session.return_value = mock_db

    mock_last_entry = MagicMock()
    mock_last_entry.year = 2026
    mock_last_entry.month = 1
    mock_db.query().order_by().first.return_value = mock_last_entry

    mock_db.query().filter_by().first.return_value = None

    update_latest_month()

    mock_fetch_rate.assert_called_once_with(2026, 2)

    added_obj = mock_db.add.call_args[0][0]
    assert isinstance(added_obj, ExchangeRate)
    assert added_obj.year == 2026
    assert added_obj.month == 2
    assert added_obj.average_rate == 3.25

    mock_db.commit.assert_called_once()

    mock_db.close.assert_called_once()


@patch("app.update_exchange.fetch_latest_rate")
@patch("app.update_exchange.SessionLocal")
def test_update_latest_month_no_last_entry(mock_session, mock_fetch_rate):
    mock_fetch_rate.return_value = 3.5

    mock_db = MagicMock()
    mock_session.return_value = mock_db

    mock_db.query().order_by().first.return_value = None

    mock_db.query().filter_by().first.return_value = None

    update_latest_month()

    added_obj = mock_db.add.call_args[0][0]
    assert isinstance(added_obj, ExchangeRate)
    assert added_obj.average_rate == 3.5

    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()
