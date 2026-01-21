from app.scheduler import run_monthly_update


def test_run_monthly_update_calls_update(mock_db, monkeypatch):
    monkeypatch.setattr("app.scheduler.SessionLocal", lambda: mock_db)
    monkeypatch.setattr("app.scheduler.update_latest_month", lambda db: None)

    run_monthly_update()

    mock_db.close.assert_called_once()
