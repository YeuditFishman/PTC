from data_utils import compute_diff_matrix, fetch_data, forecast_next_month, multiply_matrices
from viz_utils import plot_line, plot_bar_highlight, styled_table
import streamlit as st

st.title("PTC Exchange Rates - Part B")

df = fetch_data()

st.subheader("Average Exchange Rate by Month")
plot_line(df)

st.subheader("Exchange Rate Table with Colors")
st.dataframe(styled_table(df))

st.subheader("Highlight Specific Month")
search_month = st.selectbox("Choose Month", df['year_month'])
highlighted = df['year_month'] == search_month
plot_bar_highlight(df, highlighted)

st.subheader("Sort Data")
sort_option = st.selectbox("Sort by", ["month", "average_rate"])
ascending = st.checkbox("Ascending", value=True)
sorted_df = df.sort_values(
    by="month" if sort_option == "month"
    else "average_rate", ascending=ascending
)
st.dataframe(sorted_df[['year_month', 'average_rate']])

st.subheader("Forecast Next Month")
next_year, next_month, forecast = forecast_next_month(df)
st.write(f"Forecast for {next_year}-{next_month:02d}: {forecast:.3f}")

st.subheader("Part C: Difference and Product Matrix")

if st.button("Show Part C Matrix"):
    diff_matrix = compute_diff_matrix(df)
    product_matrix = multiply_matrices(df)
    
    st.subheader("Difference Matrix (Actual - Forecast)")
    st.dataframe(diff_matrix.style.background_gradient(cmap='coolwarm'))
    
    st.subheader("Product Matrix (Part B * Difference)")
    st.dataframe(product_matrix.style.background_gradient(cmap='coolwarm'))
