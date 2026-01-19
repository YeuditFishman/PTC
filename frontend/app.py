import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import requests

BACKEND_URL = "http://backend:8000/api/rates"

@st.cache_data(ttl=300)
def fetch_data():
    response = requests.get(BACKEND_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['year_month'] = df.apply(lambda x: f"{int(x['year'])}-{int(x['month']):02d}", axis=1)
    return df

df = fetch_data()

st.title("PTC Exchange Rates - Part B")

# -----------------------
# 1. Average Graph by Months
# -----------------------
st.subheader("Average Exchange Rate by Month")
plt.figure(figsize=(10,5))
sns.lineplot(x='year_month', y='average_rate', data=df, marker='o')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# -----------------------
# 2. Table with Color Rating
# -----------------------
def color_rate(val):
    if val == df['average_rate'].max():
        return 'background-color: green; color: white'
    elif val == df['average_rate'].min():
        return 'background-color: red; color: white'
    else:
        return ''

st.subheader("Exchange Rate Table with Colors")
styled_table = df[['year_month','average_rate']].style.applymap(color_rate, subset=['average_rate'])
st.dataframe(styled_table)

# -----------------------
# 3. Search and Highlight Month
# -----------------------
st.subheader("Highlight Specific Month")
search_month = st.selectbox("Choose Month", df['year_month'])
highlighted = df['year_month'] == search_month

plt.figure(figsize=(10,5))
sns.barplot(x='year_month', y='average_rate', data=df, palette=['orange' if h else 'blue' for h in highlighted])
plt.xticks(rotation=45)
st.pyplot(plt)

# -----------------------
# 4. Sort Options
# -----------------------
st.subheader("Sort Data")
sort_option = st.selectbox("Sort by", ["month", "average_rate"])
ascending = st.checkbox("Ascending", value=True)
sorted_df = df.sort_values(by="month" if sort_option=="month" else "average_rate", ascending=ascending)
st.dataframe(sorted_df[['year_month','average_rate']])

# -----------------------
# 5. Forecast Next Month
# -----------------------
st.subheader("Forecast Next Month")
last_3_avg = df.tail(3)['average_rate'].mean()
next_month = df['month'].iloc[-1] + 1
next_year = df['year'].iloc[-1]
if next_month > 12:
    next_month = 1
    next_year += 1

st.write(f"Forecast for {next_year}-{next_month:02d}: {last_3_avg:.3f}")
