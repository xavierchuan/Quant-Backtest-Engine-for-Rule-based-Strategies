# main.py
import argparse
import os
import pandas as pd
import yfinance as yf
from engine.backtester import Backtester
from strategies.moving_average import MovingAverageCrossStrategy
from strategies.mean_reversion import MeanReversionStrategy

# CLI 参数解析
parser = argparse.ArgumentParser(description="Run quant backtest engine")
parser.add_argument('--strategy', type=str, default='moving_average', help='Strategy name: moving_average / mean_reversion')
parser.add_argument('--ticker', type=str, default='BTC-USD', help='Ticker symbol like BTC-USD, ETH-USD, MSFT')
parser.add_argument('--start', type=str, default='2021-01-01', help='Start date (YYYY-MM-DD)')
parser.add_argument('--end', type=str, default='2023-12-31', help='End date (YYYY-MM-DD)')
args = parser.parse_args()

os.makedirs("output", exist_ok=True)

# 下载数据
data = yf.download(args.ticker, start=args.start, end=args.end)

# 统一处理：无论是否 MultiIndex，最终都保留为 ['Close'] 列
if isinstance(data.columns, pd.MultiIndex):
    data = data['Close']
    if isinstance(data, pd.Series):
        data = data.to_frame()
    data.columns = ['Close']
else:
    if 'Close' in data.columns:
        data = data[['Close']]
    else:
        raise ValueError("No 'Close' column found in downloaded data.")

data = data.dropna()

# 选择策略
if args.strategy == 'moving_average':
    strategy = MovingAverageCrossStrategy(short_window=20, long_window=50)
elif args.strategy == 'mean_reversion':
    strategy = MeanReversionStrategy(window=20, threshold=0.02)
else:
    raise ValueError(f"Unknown strategy: {args.strategy}")

# 运行回测
backtester = Backtester(data, strategy)
backtester.run()
backtester.plot(ticker=args.ticker, strategy_name=args.strategy, start_date=args.start, end_date=args.end)
backtester.save_metrics(f"output/metrics_{args.ticker}_{args.strategy}_{args.start}_{args.end}.csv")