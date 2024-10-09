import streamlit as st
import yfinance as yf
import quantstats as qs
import matplotlib.pyplot as plt

# Function to get stock data from Yahoo Finance
def get_stock_data(symbol, period='2y'):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data

# Function to display performance metrics
def display_metrics(data):
    st.write("### Performance Metrics")
    st.write(f"Start Date: {data.index.min().date()}")
    st.write(f"End Date: {data.index.max().date()}")
    st.write(f"Total Return: {((data['Close'][-1] / data['Close'][0]) - 1) * 100:.2f}%")
    st.write(f"Average Daily Return: {data['Close'].pct_change().mean() * 100:.2f}%")
    st.write(f"Volatility (Standard Deviation): {data['Close'].pct_change().std() * 100:.2f}%")
    st.write(f"Max Drawdown: {((data['Close'].min() / data['Close'].max()) - 1) * 100:.2f}%")

# Function to display Quantstats report or simple plots
def display_quantstats_summary(data, symbol):
    returns = data['Close'].pct_change().dropna()

    # Show a rolling returns plot
    st.write("### Rolling Returns")
    fig, ax = plt.subplots()
    qs.plots.rolling_returns(returns, ax=ax)
    st.pyplot(fig)

    # Show a simple summary
    st.write("### QuantStats Summary")
    st.write(qs.reports.metrics(returns))

# Streamlit app
st.title("Stock Data Viewer")
st.write("Fetch stock data for the last 2 years and view performance metrics.")

# Search bar for stock symbol
symbol = st.text_input("Enter a stock symbol (e.g., AAPL, TSLA, MSFT):")

if symbol:
    try:
        # Fetch stock data
        data = get_stock_data(symbol)
        
        if not data.empty:
            # Plot the stock data
            st.write(f"### Price data for {symbol}")
            st.line_chart(data['Close'])

            # Display performance metrics
            display_metrics(data)

            # Display the QuantStats summary
            display_quantstats_summary(data, symbol)
        else:
            st.error("No data found for the entered symbol.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
