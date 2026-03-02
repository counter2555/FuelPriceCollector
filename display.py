import streamlit as st
import pandas as pd
from db import DBHandler

db_handler = DBHandler(db_url="./fuel_prices.db")
price_df = db_handler.get_prices()

# 1. Ensure your date/time column is the index
# Replace 'timestamp' with the actual name of your time column
price_df['timestamp'] = pd.to_datetime(price_df['timestamp'])
price_df = price_df.set_index('timestamp')

# 2. Pivot the data: Rows = Time, Columns = Stations, Values = Price
# This creates a table where each column is a line on the chart
chart_data = price_df.pivot(columns='station_name', values='price')

# Streamlit Page Setup
st.set_page_config(page_title="Treibstoff Dashboard", page_icon="⛽", layout="wide")
st.title("Treibstoff Preisvergleich")

# 3. Plot everything at once
# st.line_chart automatically uses the index for X and columns for the legend/Y
st.line_chart(
    chart_data
)