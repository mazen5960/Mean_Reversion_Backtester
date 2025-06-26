import yfinance as yf
import pandas as pd

start_date = "2022-01-01"
end_date = "2025-05-01"

aapl = yf.download("AAPL", start=start_date, end=end_date)
data = aapl[['Close']].reset_index()
data.columns = ['date', 'close']
data.to_csv("aapl_stock_data.csv", index=False)
