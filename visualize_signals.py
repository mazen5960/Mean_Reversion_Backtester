import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

def visualize_signals(csv_file):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    
    fig, axes = plt.subplots(3, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # Main price chart
    ax1 = axes[0]
    ax1.plot(df['date'], df['close'], label='Close Price', linewidth=2, color='blue')
    
    if 'sma_20' in df.columns:
        ax1.plot(df['date'], df['sma_20'], label='SMA 20', linewidth=1, color='orange', alpha=0.7)
    
    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']
    
    if not buy_signals.empty:
        ax1.scatter(buy_signals['date'], buy_signals['close'], 
                   marker='^', s=100, color='green', label='BUY Signal', zorder=5)
    
    if not sell_signals.empty:
        ax1.scatter(sell_signals['date'], sell_signals['close'], 
                   marker='v', s=100, color='red', label='SELL Signal', zorder=5)
    
    ax1.set_title('Stock Price with Buy/Sell Signals', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Z-score chart
    ax2 = axes[1]
    if 'z_score' in df.columns:
        ax2.plot(df['date'], df['z_score'], label='Z-Score', linewidth=1, color='purple')
        ax2.axhline(y=2, color='red', linestyle='--', alpha=0.7, label='Overbought (2)')
        ax2.axhline(y=-2, color='green', linestyle='--', alpha=0.7, label='Oversold (-2)')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.fill_between(df['date'], df['z_score'], 0, where=(df['z_score'] >= 0), 
                        alpha=0.3, color='red')
        ax2.fill_between(df['date'], df['z_score'], 0, where=(df['z_score'] < 0), 
                        alpha=0.3, color='green')
        ax2.set_ylabel('Z-Score', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    # Volume chart (if available)
    ax3 = axes[2]
    if 'volume' in df.columns:
        ax3.bar(df['date'], df['volume'], alpha=0.7, color='gray', label='Volume')
        ax3.set_ylabel('Volume', fontsize=12)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    else:
        # Performance metrics
        if not buy_signals.empty and not sell_signals.empty:
            ax3.text(0.1, 0.8, f'Total Buy Signals: {len(buy_signals)}', transform=ax3.transAxes, fontsize=12)
            ax3.text(0.1, 0.6, f'Total Sell Signals: {len(sell_signals)}', transform=ax3.transAxes, fontsize=12)
            ax3.text(0.1, 0.4, f'Signal Ratio: {len(buy_signals)/len(sell_signals):.2f}', transform=ax3.transAxes, fontsize=12)
        ax3.set_ylabel('Metrics', fontsize=12)
        ax3.set_ylim(0, 1)
    
    # Format x-axis for all subplots
    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    ax3.set_xlabel('Date', fontsize=12)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print("\n=== TRADING SIGNALS SUMMARY ===")
    print(f"Total data points: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
    
    if not buy_signals.empty:
        print(f"Buy signals: {len(buy_signals)}")
        print(f"Average buy price: ${buy_signals['close'].mean():.2f}")
    
    if not sell_signals.empty:
        print(f"Sell signals: {len(sell_signals)}")
        print(f"Average sell price: ${sell_signals['close'].mean():.2f}")
    
    if 'z_score' in df.columns:
        print(f"Z-score range: {df['z_score'].min():.2f} to {df['z_score'].max():.2f}")
        print(f"Average z-score: {df['z_score'].mean():.2f}")

def create_performance_analysis(csv_file):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate returns
    df['returns'] = df['close'].pct_change()
    df['cumulative_returns'] = (1 + df['returns']).cumprod()
    
    # Calculate strategy returns (simple example)
    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']
    
    if not buy_signals.empty and not sell_signals.empty:
        # Simple strategy: buy and hold from buy signal to sell signal
        strategy_returns = []
        for i, buy_row in buy_signals.iterrows():
            # Find next sell signal after this buy signal
            next_sell = sell_signals[sell_signals['date'] > buy_row['date']]
            if not next_sell.empty:
                sell_row = next_sell.iloc[0]
                buy_price = buy_row['close']
                sell_price = sell_row['close']
                trade_return = (sell_price - buy_price) / buy_price
                strategy_returns.append(trade_return)
        
        if strategy_returns:
            print(f"\n=== STRATEGY PERFORMANCE ===")
            print(f"Number of completed trades: {len(strategy_returns)}")
            print(f"Average trade return: {np.mean(strategy_returns):.2%}")
            print(f"Total strategy return: {np.sum(strategy_returns):.2%}")
            print(f"Win rate: {sum(1 for r in strategy_returns if r > 0) / len(strategy_returns):.2%}")

if __name__ == "__main__":
    csv_file = "signals_data.csv"
    try:
        visualize_signals(csv_file)
        create_performance_analysis(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Please make sure the CSV file exists.")
    except Exception as e:
        print(f"Error: {e}") 