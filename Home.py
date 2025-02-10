import streamlit as st



st.set_page_config(
    page_title="Stock Prize Prediction",
    page_icon=":bar_chart:",
    layout="wide"
)


st.title("Trading Guide WebApp :bar_chart:")
st.markdown("---")

st.header("We provide a platform for you to collect all information prior to investing in stocks.")

st.image("front_image.jpg")

st.markdown("## We provide the following services:")

st.markdown("### :one: Stock Analysis:")
st.write("Through this page you can see all the information about stock.")

st.markdown("### :two: Stock Comparison:")
st.write("You can compare between two stocks.")

st.markdown("### :three: Stock List:")
st.write("You can find all the Stock Ticker name here.")

st.markdown("### :four: Stock Price Prediction:")
st.write("You can explore predicted closing prices for the next 30 days based on the historical stock data and advanced forecasting models.")

st.markdown("---")

st.markdown('## :money_with_wings: Basic Trading Terms :money_with_wings:')

# Define a dictionary of terms and their descriptions
terms = {
    "RSI" : "The Relative Strength Index (RSI) is a technical indicator that helps traders determine if a stock or market is overbought or oversold. It's used to generate buy and sell signals.",

    "MACD" : "Moving Average Convergence Divergence (MACD) is a technical indicator that helps traders and investors identify trends and potential entry points for buying or selling. It is a popular tool in technical analysis.",

    "Moving Average" :"A moving average (MA) is a technical indicator that shows the average price of a security over a set period of time. It's used by traders to identify trends and make decisions about buying or selling.",

    "Market Capital": "Market capitalization, or market cap, is the total value of a company's outstanding shares. It's a financial metric that helps investors understand a company's size, stability, and growth potential.",

    "Beta": "Beta is a measure of a stock's volatility in relation to the overall market. A beta greater than 1 indicates higher volatility, while a beta less than 1 indicates lower volatility.",

    "EPS": "Earnings Per Share (EPS) is a financial metric calculated as a company's profit divided by its outstanding shares. It shows how much profit is attributed to each share of stock.",

    "PE Ratio": "The Price-to-Earnings (PE) Ratio is a valuation metric that compares a company's stock price to its earnings per share. It indicates how much investors are willing to pay per dollar of earnings.",

    "Total Revenue": "Total revenue is the total amount of money a company earns from its business operations before any expenses are deducted.",

    "Quick Ratio": "The quick ratio, also known as the acid-test ratio, measures a company's ability to meet its short-term liabilities with its most liquid assets.",

    "Revenue per share": "Revenue per share is calculated by dividing a company's total revenue by its total outstanding shares. It shows the revenue earned per share.",

    "Profit Margins": "Profit margin is a measure of profitability, calculated as net income divided by revenue. It indicates how much profit a company makes for every dollar of revenue.",

    "Debt to Equity": "The debt-to-equity ratio is a financial leverage ratio that compares a company's total liabilities to its shareholders' equity. It shows how much debt a company uses to finance its operations.",

    "Return on Equity": "Return on Equity (ROE) measures a company's profitability relative to its shareholders' equity. It shows how efficiently a company uses its equity to generate profits."
}

# Generate Markdown and write content for each term
for term, description in terms.items():
    st.markdown(f'### :large_blue_diamond: {term}: ')
    st.write(description)
