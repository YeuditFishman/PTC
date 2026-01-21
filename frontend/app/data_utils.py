import os
import pandas as pd
import requests

BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise RuntimeError("BACKEND_URL is not set")


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


def compute_diff_matrix(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['forecast'] = df['average_rate'].rolling(3).mean().shift(1)
    df['diff'] = df['average_rate'] - df['forecast']
    diff_matrix = df.pivot(index='year', columns='month', values='diff')
    diff_matrix.loc['Avg'] = diff_matrix.mean()
    return diff_matrix


def multiply_matrices(df: pd.DataFrame) -> pd.DataFrame:
    matrix_b = df.pivot(index='year', columns='month', values='average_rate')
    diff_matrix = compute_diff_matrix(df)
    common_index = matrix_b.index.intersection(diff_matrix.index)
    product_matrix = matrix_b.loc[common_index] * diff_matrix.loc[common_index]
    return product_matrix
