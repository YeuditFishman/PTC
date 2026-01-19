from .database import SessionLocal
from .models import ExchangeRate
from datetime import datetime, timedelta
import requests
import pandas as pd
from io import StringIO
from sqlalchemy.dialects.postgresql import insert

def fetch_latest_rate(year: int, month: int) -> float:
    startperiod = f"{year}-{month:02d}-01"
    endperiod = f"{year}-{month:02d}-28"
    
    url = (
        "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/"
        f"?c%5BSERIES_CODE%5D=RER_USD_ILS&format=csv&normalisefreq=M;mean"
        f"&startperiod={startperiod}&endperiod={endperiod}"
    )

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"No data available for {year}-{month:02d}: {e}")
        return None

    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    
    print("CSV Columns:", df.columns)
    print(df.head())

    latest_value = df['OBS_VALUE'].iloc[-1]
    return float(latest_value)


def update_latest_month():
    db = SessionLocal()

    last_entry = db.query(ExchangeRate).order_by(
        ExchangeRate.year.desc(),
        ExchangeRate.month.desc()
    ).first()

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

    rate = fetch_latest_rate(year, month)

    if rate is None:
        print(f"Skipping update for {year}-{month:02d}, no data available yet.")
        db.close()
        return

    existing = db.query(ExchangeRate).filter_by(year=year, month=month).first()
    if not existing:
        db.add(ExchangeRate(year=year, month=month, average_rate=rate))
        db.commit()
        print(f"Updated EXR {year}-{month:02d} = {rate}")
    else:
        print(f"EXR {year}-{month:02d} already exists, skipping.")

    db.close()

    print(f"Updated EXR {year}-{month:02d} = {rate}")



if __name__ == "__main__":
    update_latest_month()
