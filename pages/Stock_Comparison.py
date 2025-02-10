import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime

st.set_page_config(
    page_title="Stock Comparison",
    page_icon=":chart:",
    layout="wide"
)

# Page title
st.markdown('<h1 style="color:#65FE08;">Stocks Comparison 💹</h1>', unsafe_allow_html=True)
st.markdown("---")

# Columns for input fields
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
today = datetime.date.today()

with col1:
    ticker1 = st.text_input("Ticker 1", "TCS.NS")
with col2:
    ticker2 = st.text_input("Ticker 2", "TITAN.NS")
with col3:
    ticker3 = st.text_input("Ticker 3", "")
with col4:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col5:
    end_date = st.date_input("Choose End Date", today)

# Data download and processing
if ticker3.strip() == "":
    data1 = yf.download(ticker1, start=start_date, end=end_date)
    data2 = yf.download(ticker2, start=start_date, end=end_date)

    # Extracting Close prices
    data1 = data1[['Close']].rename(columns={'Close': 'ticker1_close'})
    data2 = data2[['Close']].rename(columns={'Close': 'ticker2_close'})

    # Merging dataframes
    merged_data = pd.concat([data1, data2], axis=1).dropna().reset_index().round(2)
else:
    data1 = yf.download(ticker1, start=start_date, end=end_date)
    data2 = yf.download(ticker2, start=start_date, end=end_date)
    data3 = yf.download(ticker3, start=start_date, end=end_date)

    # Extracting Close prices
    data1 = data1[['Close']].rename(columns={'Close': 'ticker1_close'})
    data2 = data2[['Close']].rename(columns={'Close': 'ticker2_close'})
    data3 = data3[['Close']].rename(columns={'Close': 'ticker3_close'})

    # Merging dataframes
    merged_data = pd.concat([data1, data2, data3], axis=1).dropna().reset_index().round(2)

# Display merged data
st.markdown("### Comparison in Tabular form:")
st.dataframe(merged_data, use_container_width=True)

# Button to toggle showing data points
show_data_points = st.checkbox("Show Data Points", value=False)

# Plotting with Matplotlib
sns.set_style('darkgrid')
plt.figure(figsize=(10, 5))
plt.plot(merged_data['Date'], merged_data["ticker1_close"], label=ticker1, color='red', linewidth=1, marker='o' if show_data_points else '')
plt.plot(merged_data['Date'], merged_data['ticker2_close'], label=ticker2, color='green', linewidth=1, marker='o' if show_data_points else '')
if ticker3.strip():
    plt.plot(merged_data['Date'], merged_data['ticker3_close'], label=ticker3, color='blue', linewidth=1, marker='o' if show_data_points else '')


plt.title('Stock Prices Comparison Over Time', fontsize=18, fontweight="bold")
plt.xlabel("Date & Time", fontsize=15)
plt.ylabel("Price",fontsize=15)
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
st.pyplot(plt)
