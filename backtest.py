# Write a Python script using yfinance to download AAPL stock data from 2022-01-01 to 2025-05-01 and save it as a CSV with columns: date, close

import yfinance as yf
import pandas as pd
from datetime import datetime

def download_aapl_data():
    """
    Download AAPL stock data from 2022-01-01 to 2025-05-01 and save as CSV
    """
    start_date = "2022-01-01"
    end_date = "2025-05-01"
    
    print(f"Downloading AAPL stock data from {start_date} to {end_date}...")
    aapl = yf.download("AAPL", start=start_date, end=end_date)
    
    data = aapl[['Close']].reset_index()
    data.columns = ['date', 'close']
    
    output_filename = "aapl_stock_data.csv"
    data.to_csv(output_filename, index=False)
    
    print(f"Data successfully saved to {output_filename}")
    print(f"Total records: {len(data)}")
    print(f"Date range: {data['date'].min()} to {data['date'].max()}")
    
    return data

if __name__ == "__main__":
    try:
        data = download_aapl_data()
        print("\nFirst 5 rows of the data:")
        print(data.head())
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Make sure you have yfinance installed: pip install yfinance")


