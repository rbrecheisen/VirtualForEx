import pandas as pd
import mplfinance as mpf


START_DATE = "2024-10-01"
END_DATE = "2025-02-01"
STYLE=  'yahoo'


df = pd.read_csv("G:\\My Drive\\data\\MetaTrader5\\EURUSDDaily.csv", parse_dates=['Date'])
df.set_index('Date', inplace=True)
filtered_df = df.loc[START_DATE:END_DATE]

mpf.plot(filtered_df, type='candle', style=STYLE)