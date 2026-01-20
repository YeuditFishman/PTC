from dotenv import load_dotenv
import os
import pandas as pd
import requests

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")


def fetch_data() -> pd.DataFrame:
    response = requests.get(BACKEND_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['year_month'] = df.apply(
        lambda x: f"{int(x['year'])}-{int(x['month']):02d}", axis=1
    )

    return df


def forecast_next_month(df: pd.DataFrame) -> tuple[int, int, float]:
    last_3_avg = df.tail(3)['average_rate'].mean()
    next_month = df['month'].iloc[-1] + 1
    next_year = df['year'].iloc[-1]
    if next_month > 12:
        next_month = 1
        next_year += 1
    return next_year, next_month, last_3_avg
