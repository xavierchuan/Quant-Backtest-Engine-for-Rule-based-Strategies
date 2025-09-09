# run_default_batch.py

import os
import pandas as pd
import yfinance as yf
from engine.backtester import Backtester
from strategies.moving_average import MovingAverageCrossStrategy
from strategies.mean_reversion import MeanReversionStrategy

# === 清洗数据函数 ===
def clean_data(df):
    df = df[['Close']].copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    df.columns.name = None
    df.index = pd.to_datetime(df.index)
    return df

# === 默认参数设置 ===
start_date = "2021-01-01"
end_date = "2023-12-31"
assets = ["BTC-USD", "ETH-USD", "MSFT", "AAPL", "TSLA"]
strategies = {
    "moving_average": MovingAverageCrossStrategy(short_window=20, long_window=50),
    "mean_reversion": MeanReversionStrategy(window=20, threshold=0.02),
}

# 创建输出文件夹
os.makedirs("output", exist_ok=True)

# 收集所有指标汇总
all_metrics = []

# === 批量回测循环 ===
for ticker in assets:
    print(f"\n🔍 Downloading data for: {ticker}")
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty or 'Close' not in data.columns:
        print(f"⚠️ 数据获取失败或无 'Close' 列: {ticker}")
        continue

    data = clean_data(data)

    for strategy_name, strategy_obj in strategies.items():
        print(f"🚀 Running backtest: {ticker} + {strategy_name}")

        backtester = Backtester(data, strategy_obj)
        backtester.run()

        # 输出图表
        backtester.plot(
            ticker=ticker,
            strategy_name=strategy_name,
            start_date=start_date,
            end_date=end_date
        )

        # 输出 CSV 文件（每个组合单独保存）
        metrics_path = f"output/metrics_{ticker}_{strategy_name}_{start_date[:4]}-{end_date[:4]}.csv"
        backtester.save_metrics(metrics_path)

        # 收集所有组合指标到汇总列表中
        all_metrics.append({
            "Ticker": ticker,
            "Strategy": strategy_name,
            "Start": start_date,
            "End": end_date,
            "Total Return": backtester.total_return,
            "Annualized Return": backtester.annual_return,
            "Max Drawdown": backtester.max_drawdown,
            "Sharpe Ratio": backtester.sharpe_ratio
        })

# === 保存总指标表 ===
summary_df = pd.DataFrame(all_metrics)
summary_df.to_csv("output/summary_metrics_all.csv", index=False)
print("\n✅ Batch backtest completed. All results saved to /output")