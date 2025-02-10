import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA

# Get stock data
def get_data(ticker):
    stock_data = yf.download(ticker, start='2020-01-01')
    return stock_data[['Close']]

# Stationarity test (ADF test)
def stationary_checks(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)
    return p_value

# Get rolling mean
def get_rolling_mean(close_price):
    return close_price.rolling(window=20).mean().dropna()

# Get differencing order
def get_differencing_order(close_price):
    p_value = stationary_checks(close_price)
    d = 0
    while p_value > 0.5:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_checks(close_price)
    return d

# Fit ARIMA model
def fit_model(data, differencing_order):
    model = ARIMA(data, order=(30, differencing_order, 30))
    model_fit = model.fit()
    forecast_steps = 30
    forecast = model_fit.forecast(steps=forecast_steps)
    return forecast

# Evaluate model (RMSE score)
def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]  # Match lengths of train and test data
    predictions = fit_model(train_data, differencing_order)
    rmse = np.sqrt(mean_squared_error(test_data, predictions))  # Now both have length 30
    return round(rmse, 2)

# Scale data
def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data, scaler

# Get forecast
def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])
    return forecast_df

# Inverse scaling
def inverse_scaling(scaler, scaled_data):
    return scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
