import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pages.utils.model_train import get_data, get_differencing_order, get_forecast, get_rolling_mean, scaling, evaluate_model, inverse_scaling
from pages.utils.plotly_figure import plotly_table

st.set_page_config(page_title="Stock Prediction", page_icon="chart_with_downwards_trend", layout="wide")
st.markdown('<h1 style="color:#65FE08;">Stock Prediction</h1>', unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input('Stock Ticker', 'TCS.NS')

rmse = 0
st.markdown(f'### Predicting Next 30 Days Close Price for: <span style= "color:#FFD700"> {ticker} </span>', unsafe_allow_html=True)

# Fetch stock data and perform preprocessing
close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.markdown(f'<span style= "color:#FFD700">Model RMSE Score:</span> {rmse}', unsafe_allow_html=True)
forecast = get_forecast(scaled_data, differencing_order)

# Inverse transform the forecasted values
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

st.write('#### Forecast Data (Next 30 days)')
# fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
# st.dataframe(rolling_price, use_container_width=True)
st.dataframe(forecast, use_container_width=True)
# fig_tail.update_layout(height=220)
# st.plotly_chart(fig_tail, use_container_width=True)

# Concatenate historical data with forecasted data
# new_forecast = pd.concat([rolling_price, forecast])

# ✅ **Matplotlib Plot**
fig, (ax1,ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

# Plot historical & predicted data stock prices in the first subplot
ax1.plot(rolling_price.index, rolling_price['Close'], label="Historical Data", color="blue", linewidth=2)
ax1.plot(forecast.index, forecast['Close'], label="Predicted Data", color="red", linewidth=2)
ax1.set_title(f"Stock Prices prediction for {ticker}", fontsize=14)
ax1.set_ylabel("Close Price", fontsize=12)
ax1.legend()
ax1.grid(True)

# Plot predicted stock prices in the second subplot
ax2.plot(rolling_price.index, rolling_price['Close'], label="Historical Data", color="blue", linewidth=2)
ax2.set_title(f"Historical Stock Prices for {ticker}", fontsize=14)
ax2.set_xlabel("Date", fontsize=12)
ax2.set_ylabel("Close Price", fontsize=12)
ax2.legend()
ax2.grid(True)


ax3.plot(forecast.index, forecast['Close'], label="Predicted Data", color="red", marker='o', linewidth=2)
ax3.set_title(f"Predicted Stock Prices for {ticker}", fontsize=14)
ax3.set_xlabel("Date", fontsize=12)
ax3.set_ylabel("Close Price", fontsize=12)
ax3.legend()
ax3.grid(True)
plt.tight_layout()  # Adjust layout for better spacing

# Display the plot in Streamlit
st.pyplot(fig)
