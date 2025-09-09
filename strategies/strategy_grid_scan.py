# strategies/strategy_grid_scan.py

import os
import sys
import pandas as pd
import yfinance as yf

# 加入项目根目录到 sys.path，确保可以 import 本地模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strategies.moving_average import MovingAverageCrossStrategy
from engine.backtester import Backtester

# 🔧 数据清洗函数，处理 MultiIndex 和非 Close 列问题
def clean_data(df):
    print("🧹 Running clean_data")
    print("🔍 Raw columns:", df.columns)

    # 展平多层列名：保留第 0 层（'Price'）
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    print("✅ Flattened columns:", df.columns)

    if 'Close' in df.columns:
        df = df[['Close']].copy()
    else:
        raise KeyError("❌ Data does not contain 'Close' column after flattening.")
    
    df.columns.name = None
    df.index = pd.to_datetime(df.index)
    return df
# 参数网格
short_windows = [10, 20, 30]
long_windows = [50, 100, 150]

# 股票和时间范围
ticker = "AAPL"
start_date = "2021-01-01"
end_date = "2023-12-31"

# 下载并清洗数据
print(f"📥 Downloading data for {ticker}")
data = yf.download(ticker, start=start_date, end=end_date)
data = clean_data(data)  # 调用 clean_data 确保只有 Close 一列
print("📊 Final data preview:\n", data.head())

# 创建输出目录
os.makedirs("output", exist_ok=True)

# 存储每组结果
results = []

# 遍历参数组合
for short in short_windows:
    for long in long_windows:
        if short >= long:
            continue  # 忽略非法组合

        print(f"🧪 Testing: short={short}, long={long}")
        strategy = MovingAverageCrossStrategy(short_window=short, long_window=long)
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

# 保存为 CSV
df = pd.DataFrame(results)
df.to_csv("output/grid_scan_results.csv", index=False)
print("\n✅ Grid scan completed. Results saved to output/grid_scan_results.csv")