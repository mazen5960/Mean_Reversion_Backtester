# Mean_Reversion_Backtester
Backtesting and Analyzing a Mean Reversion Trading Strategy using SQL.


## Strategy Overview

The system identifies buy and sell signals based on deviations from the 20-day simple moving average (SMA), using Z-score logic:

- Buy when the price falls significantly below its 20-day SMA
- Sell when the price rises significantly above its 20-day SMA

## Tech Stack

- PostgreSQL (via pgAdmin) for data storage and analysis
- Python (Matplotlib) for visualization
- VSCode for development

## Key Features

- SQL queries for:
  - 20-day moving average (SMA)
  - Rolling standard deviation
  - Z-score for signal generation
- Python script to plot price, SMA, and signal points

## Files

- `download_data.py` – Downloads AAPL data from Yahoo Finance
- `visualize_signals.py` – Visualizes strategy outputs
- PostgreSQL `prices` table – Stores historical stock data with calculated indicators

## Next Steps

- Add performance metrics (e.g., cumulative returns)
- Expand to support multiple stocks
- Optional: build a basic dashboard for interaction

---

Built by Mazen Chouayeb | Summer 2025

