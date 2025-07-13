import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load your price data
df = pd.read_csv("G:\\My Drive\\data\\MetaTrader5\\EURUSDDaily.csv", parse_dates=['Date'])

# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']
)])

# Add range slider and zoom/pan tools
fig.update_layout(
    xaxis_rangeslider_visible=True,
    yaxis_fixedrange=False,
    title="Candlestick Chart from CSV",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark"
)

fig.show()
