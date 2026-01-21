import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def color_rate(val, df: pd.DataFrame) -> str:
    if val == df['average_rate'].max():
        return 'background-color: green; color: white'
    elif val == df['average_rate'].min():
        return 'background-color: red; color: white'
    return ''


def plot_bar_highlight(df: pd.DataFrame, highlight_mask: pd.Series):
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x='year_month',
        y='average_rate',
        data=df,
        palette=['orange' if h else 'blue' for h in highlight_mask]
    )
    plt.xticks(rotation=45)
    st.pyplot(plt)


def plot_line(df: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='year_month', y='average_rate', data=df, marker='o')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)


def styled_table(df: pd.DataFrame):
    return df[['year_month', 'average_rate']].style.applymap(
        lambda val: color_rate(val, df), subset=['average_rate']
    )
