# strategies/strategy_grid_scan_batch.py

import os
import sys
import pandas as pd
import yfinance as yf

# 设置路径以导入本地模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strategies.moving_average import MovingAverageCrossStrategy
from engine.backtester import Backtester

# 可选资产标的
tickers = ["AAPL", "TSLA", "BTC-USD", "ETH-USD"]
short_windows = [10, 20, 30]
long_windows = [50, 100, 150]

def clean_data(df):
    df.columns.name = None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    if "Close" not in df.columns:
        raise ValueError("Missing 'Close' column in data.")
    df = df[["Close"]].copy().dropna()
    df.index = pd.to_datetime(df.index)
    return df

# 主循环
for ticker in tickers:
    print(f"\n📥 Downloading data for {ticker}")
    data = yf.download(ticker, start="2021-01-01", end="2023-12-31")
    data = clean_data(data)

    results = []
    for short in short_windows:
        for long in long_windows:
            if short >= long:
                continue
            print(f"🧪 [{ticker}] Testing: short={short}, long={long}")
            strategy = MovingAverageCrossStrategy(short, long)
            backtester = Backtester(data, strategy)
            backtester.run()
            results.append({
                "Short Window": short,
                "Long Window": long,
                "Total Return": backtester.total_return,
                "Annualized Return": backtester.annual_return,
                "Max Drawdown": backtester.max_drawdown,
                "Sharpe Ratio": backtester.sharpe_ratio
            })

    # 保存结果
    output_dir = f"output/{ticker}"
    os.makedirs(output_dir, exist_ok=True)
    pd.DataFrame(results).to_csv(f"{output_dir}/grid_scan_results.csv", index=False)
    print(f"✅ Saved results to {output_dir}/grid_scan_results.csv")