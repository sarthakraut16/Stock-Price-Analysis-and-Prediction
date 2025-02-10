import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Set Streamlit Page Config
st.set_page_config(
    page_title="Stock List",
    page_icon=":memo:",
    layout="wide"
)

#page title
st.markdown('<h1 style="color:#65FE08;">Stock Ticker List 💵</h1>', unsafe_allow_html=True)
st.markdown("---")

# Load the CSV file
file_path = 'D:\\Stock Price Prediction\\EQUITY_L.csv'
ticker_list = pd.read_csv(file_path)

# Select Relevant Columns
ticker_list = ticker_list[['NAME OF COMPANY', 'YahooEquiv']]

# 🔍 Search Box
search_query = st.text_input("Search for a company:", "").strip().lower()

# Filter the DataFrame Based on Search Query
if search_query:
    filtered_df = ticker_list[ticker_list['NAME OF COMPANY'].str.lower().str.contains(search_query, na=False)]
else:
    filtered_df = ticker_list  # Show full list if no search input

# Create Table Using Plotly
fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(filtered_df.columns),
        fill_color="#FFD700",  # Header background color
        font=dict(color="black", size=18),  # Header font color & size
        align="left",
        height=40
    ),
    cells=dict(
        values=[filtered_df[col] for col in filtered_df.columns],
        fill_color=["#2E2E2E", "#333333"],  # Alternating row colors
        font=dict(color="white", size=18),  # Cell text color & size
        align="left",
        height=40
    )
)])

# Adjust Layout
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=800)

# Display Table in Streamlit
st.plotly_chart(fig, use_container_width=True)
