import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to generate random stock data
def generate_random_stock_data(symbol, days=365):
    # Generate a date range
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    # Generate random stock prices
    prices = np.random.normal(loc=100, scale=10, size=days).cumsum()  # Random walk
    data = pd.DataFrame(data={'Date': dates, 'Close': prices}).set_index('Date')
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

# Streamlit app
st.title("Random Stock Data Viewer")
st.write("Display random stock data and performance metrics.")

# Search bar for stock symbol
symbol = st.text_input("Enter a stock symbol (e.g., RANDOM):", value="RANDOM")

if symbol:
    # Generate random stock data
    data = generate_random_stock_data(symbol)

    if not data.empty:
        # Plot the stock data
        st.write(f"### Price data for {symbol}")
        st.line_chart(data['Close'])

        # Display performance metrics
        display_metrics(data)
