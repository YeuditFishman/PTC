from datetime import datetime, timedelta
from io import StringIO
import logging
from .models import ExchangeRate
import os
import pandas as pd
import requests

logger = logging.getLogger(__name__)

BOI_BASE_URL = os.getenv("BOI_BASE_URL")
BOI_DATAFLOW = os.getenv("BOI_DATAFLOW")
BOI_FORMAT = os.getenv("BOI_FORMAT")
BOI_SERIES_CODE = os.getenv("BOI_SERIES_CODE")


def add_rate_if_missing(db, year: int, month: int, rate: float):
    existing = db.query(ExchangeRate).filter_by(year=year, month=month).first()
    if not existing:
        db.add(ExchangeRate(year=year, month=month, average_rate=rate))
        db.commit()
        logger.info(f"Updated EXR {year}-{month:02d} = {rate}")
    else:
        logger.info(f"EXR {year}-{month:02d} already exists, skipping.")


def fetch_latest_rate(year: int, month: int) -> float | None:
    startperiod = f"{year}-{month:02d}-01"
    endperiod = f"{year}-{month:02d}-28"

    url = (
        f"{BOI_BASE_URL}/{BOI_DATAFLOW}/"
        f"?c[SERIES_CODE]={BOI_SERIES_CODE}"
        f"&format={BOI_FORMAT}"
        "&normalisefreq=M;mean"
        f"&startperiod={startperiod}&endperiod={endperiod}"
    )

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
    except requests.HTTPError as error:
        logger.info(f"No data available for {year}-{month:02d}: {error}")
        return None

    df = pd.read_csv(StringIO(response.text))
    return float(df["OBS_VALUE"].iloc[-1])


def next_month(last_entry: ExchangeRate | None) -> tuple[int, int]:
    if last_entry:
        year = last_entry.year
        month = last_entry.month + 1
        if month > 12:
            month = 1
            year += 1
    else:
        target_date = datetime.now().replace(day=1) - timedelta(days=1)
        year = target_date.year
        month = target_date.month
    return year, month


def update_latest_month(db):
    last_entry = db.query(ExchangeRate).order_by(
        ExchangeRate.year.desc(), ExchangeRate.month.desc()
    ).first()
    year, month = next_month(last_entry)
    rate = fetch_latest_rate(year, month)
    if rate is None:
        logger.error(f"{year}-{month:02d}, no data available yet.")
        return
    add_rate_if_missing(db, year, month, rate)
