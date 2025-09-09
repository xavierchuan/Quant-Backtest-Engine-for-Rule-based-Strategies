# run_batch.py
import argparse
import os
import subprocess

# 解析 CLI 参数
parser = argparse.ArgumentParser(description="Batch run strategies on multiple tickers")
parser.add_argument('--tickers', nargs='+', required=True, help='List of tickers like BTC-USD ETH-USD AAPL')
parser.add_argument('--strategies', nargs='+', required=True, help='List of strategies like moving_average mean_reversion')
parser.add_argument('--start', type=str, default="2021-01-01", help='Start date for backtest')
parser.add_argument('--end', type=str, default="2023-12-31", help='End date for backtest')
args = parser.parse_args()

# 确保 output 文件夹存在
os.makedirs("output", exist_ok=True)

# 遍历所有策略 x 所有资产
for ticker in args.tickers:
    for strategy in args.strategies:
        print(f"\n>>> Running {strategy} on {ticker}...")
        command = [
            "python", "main.py",
            "--strategy", strategy,
            "--ticker", ticker,
            "--start", args.start,
            "--end", args.end
        ]
        subprocess.run(command)

print("\n✅ All batch jobs completed.")