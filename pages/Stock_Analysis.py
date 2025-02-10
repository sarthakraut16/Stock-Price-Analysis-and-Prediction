import streamlit as st
import pandas as pd
import yfinance as yf
import datetime 
import seaborn as sns
import plotly.graph_objects as go
import re
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import candlestick
from pages.utils.plotly_figure import close_chart
from pages.utils.plotly_figure import RSI
from pages.utils.plotly_figure import MACD
from pages.utils.plotly_figure import movingaverage
import matplotlib.pyplot as plt

#Page ke title or favicon 
st.set_page_config(
    page_title="Stock Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

#page title
st.markdown('<h1 style="color:#65FE08;">Stock Analysis 📈</h1>', unsafe_allow_html=True)
st.markdown("---")



#columns for ticker name, start date, end date
col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TATASTEEL.NS")
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year-1,today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year,today.month, today.day))



stock = yf.Ticker(ticker)
# st.write(stock.info)
st.markdown("---")

try:
#Ticker name and Sector name
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
        f'<h3><span style="color:#FFD700;">Company Name: </span> '
        f'<span style="color:white;">{stock.info["longName"]}</span></h3>',
        unsafe_allow_html=True)

    with col2:
        st.markdown(
        f'<h3><span style="color:#FFD700;">Sector: </span> '
        f'<span style="color:white;">{stock.info["sector"]}</span></h3>',
        unsafe_allow_html=True)
    


#summary of the stock
    st.markdown(f'<h3><span style="color:#FFD700;">Summary: </span></h3>'
            f'<p style="font-size:18px">{stock.info["longBusinessSummary"]}</p>', unsafe_allow_html=True)

#Fulltime employees detail
    st.markdown(
        f'<h3><span style="color:#FFD700;">Fulltime Employees: </span> '
        f'<span style="color:white;">{stock.info["fullTimeEmployees"]}</span></h3>',
        unsafe_allow_html=True)

#website link
    st.markdown(
        f'<h3><span style="color:#FFD700;">Website: </span> '
        f'<a style="color:white;" href="{stock.info["website"]}">{stock.info["website"]}</a></h3>',
        unsafe_allow_html=True)


#Stock details table
    col1, col2 = st.columns(2)


    with col1:
        df = pd.DataFrame({
            "Metric":["Market Capital", "Beta", "EPS", "PE Ratio", "Total Revenue"],
            "Value": [stock.info["marketCap"], stock.info["beta"], stock.info["trailingEps"], stock.info["trailingPE"], stock.info["totalRevenue"]]
        })
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df,use_container_width= True)

    with col2:
        df = pd.DataFrame({
            "Metric":["Currency", "Revenue per share", "Profit Margins", "Debt to Equity","Return on Equity"],
            "Value": [stock.info["currency"], stock.info["revenuePerShare"], stock.info["profitMargins"], stock.info["debtToEquity"], stock.info["returnOnEquity"]]
        })
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df,use_container_width= True)
except Exception as e:
    st.write("Error in fetching data")
    st.write(e)



st.markdown("---")



# download from start date to end date using yf
data = yf.download(ticker, start=start_date, end=end_date)



# daily change in stock, prev open , prev close
daily_change = data["Close"].iloc[-1] - data["Close"].iloc[-2]
prev_close = data["Close"].iloc[-1]
prev_open = data["Open"].iloc[-1]

col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.markdown(f'<h4><span style="color:#FFD700;">Daily Change: </span><br>{str(round(daily_change[0],2))}</h4>', unsafe_allow_html=True )
with col2:
    st.markdown(f'<h4><span style="color:#FFD700;">Previous Close: </span><br>{round(prev_close[0],2)}</h4>', unsafe_allow_html=True )
with col3:
    st.markdown(f'<h4><span style="color:#FFD700;">Previous Open: </span><br>{round(prev_open[0],2)}</h4>', unsafe_allow_html=True )



# last 10 days stock data table
# last_10_df = data.tail(10)  # Get the last 10 rows

st.markdown("<h3>Stock Data:</h3>",unsafe_allow_html=True)
st.dataframe(data, use_container_width=True)  # Built-in DataFrame visualization



# buttons for the chart
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])
num_period = ''
with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1mo'):
        num_period = '1mo'
with col3:
    if st.button('6mo'):
        num_period = '6mo'
with col4:
    if st.button('1y'):
        num_period = '1y'
with col5:
    if st.button('3y'):
        num_period = '3y'
with col6:
    if st.button('5y'):
        num_period = '5y'
with col7:
    if st.button('MAX'):
        num_period = 'max'



# dropdown menue for charts
col1, col2, col3 = st.columns([1,1,4])

with col1:
    chart_type = st.selectbox("", ("Candle", "Line"))
with col2:
    if chart_type == "Candle":
        indicator = st.selectbox("", ('RSI', 'MACD'))
    else:
        indicator = st.selectbox("", ('RSI', 'Moving Average',"MACD"))



# chart for the stocks
ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period = 'max') 
data1 = ticker_.history(period = 'max') 
if num_period == '':
    if chart_type=='Candle' and indicator == 'RSI':
        st.markdown('<h3>Candle Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.markdown('<h3>RSI Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Candle' and indicator == 'MACD':
        st.markdown('<h3>Candle Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.markdown('<h3>MACD Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicator == 'RSI':
        st.markdown('<h3>Line Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.markdown('<h3>RSI Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicator == 'Moving Average':
        st.markdown('<h3>Line Chart with Moving Average</h3>', unsafe_allow_html=True)
        st.plotly_chart(movingaverage(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicator =='MACD':
        st.markdown('<h3>Line Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.markdown('<h3>MACD Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

else:
    if chart_type=='Candle' and indicator == 'RSI':
        st.markdown('<h3>Candle Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(candlestick(data1, num_period), use_container_width=True)
        st.markdown('<h3>RSI Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(RSI(data1, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicator == 'MACD':
        st.markdown('<h3>Candle Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(candlestick(data1, num_period), use_container_width=True)
        st.markdown('<h3>MACD Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(MACD(data1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicator == 'RSI':
        st.markdown('<h3>Line Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
        st.markdown('<h3>RSI Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(RSI(data1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicator == 'Moving Average':
        st.markdown('<h3>Line Chart with Moving Average</h3>', unsafe_allow_html=True)
        st.plotly_chart(movingaverage(data1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicator =='MACD':
        st.markdown('<h3>Line Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
        st.markdown('<h3>MACD Chart</h3>', unsafe_allow_html=True)
        st.plotly_chart(MACD(data1, num_period), use_container_width=True)
