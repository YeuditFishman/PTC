from app.database import engine
from app.startup import startup_event
import pytest
from unittest.mock import patch


def test_startup_event_success():
    with patch("app.startup.Base.metadata.create_all") as mock_create_all:
        startup_event()
        mock_create_all.assert_called_once_with(bind=engine)


def test_startup_event_retries_and_fail():
    with patch(
        "app.startup.Base.metadata.create_all",
        side_effect=Exception("fail")
    ):
        with pytest.raises(RuntimeError, match="Database is not available"):
            startup_event()
