from app.db_utils import insert_exchange_rates


def test_insert_exchange_rates_adds_only_new(mock_db):
    mock_db.query().filter_by().first.side_effect = [None, True]

    data = [
        (2026, 1, 3.12),
        (2026, 2, 3.25)
    ]

    insert_exchange_rates(mock_db, data)

    assert mock_db.add.call_count == 1
    mock_db.commit.assert_called_once()
