import pandas as pd
import mplfinance as mpf


df = pd.read_csv("G:\\My Drive\\data\\MetaTrader5\\EURUSDDaily.csv", parse_dates=['Date'])
df.set_index('Date', inplace=True)

mpf.plot(df, type='candle', style='charles')