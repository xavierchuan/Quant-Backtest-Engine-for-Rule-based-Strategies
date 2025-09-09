# strategy_param_optimizer.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
import numpy as np
import pandas as pd
import yfinance as yf

from scipy.optimize import minimize
from engine.backtester import Backtester
from utils.clean_data import clean_data
from strategies.moving_average import MovingAverageCrossStrategy

# === 配置 ===
ticker = "AAPL"
start_date = "2021-01-01"
end_date = "2023-01-01"
data_dir = f"output/{ticker}"
os.makedirs(data_dir, exist_ok=True)

# === 下载并清洗数据 ===
print(f"📥 Downloading data for {ticker}")
data = yf.download(ticker, start=start_date, end=end_date)
data = clean_data(data)
data.index = pd.to_datetime(data.index)

# === 目标函数：最小化 -Sharpe Ratio（最大化 Sharpe） ===
def objective(params):
    short_window, long_window = int(params[0]), int(params[1])
    
    if short_window >= long_window:
        return np.inf  # ❌ 不合法的组合
    
    strategy = MovingAverageCrossStrategy(short_window, long_window)  # ✅ 创建策略对象
    bt = Backtester(data, strategy)
    bt.run()

    sharpe = bt.sharpe_ratio
    return -sharpe  # ❗最大化 Sharpe → 最小化负值

# === 参数边界 ===
bounds = [(5, 50), (20, 200)]
initial_guess = [10, 100]

# === 执行优化 ===
print("\n⚙️ Running optimization...")
result = minimize(
    objective,
    x0=initial_guess,
    bounds=bounds,
    method="L-BFGS-B",
    options={"disp": True}
)

# === 输出最佳参数和结果 ===
best_short, best_long = int(result.x[0]), int(result.x[1])
print("\n✅ Optimization completed!")
print(f"Best Parameters: short_window = {best_short}, long_window = {best_long}")

# === 重新运行并保存完整指标 ===
best_strategy = MovingAverageCrossStrategy(best_short, best_long)
bt = Backtester(data, best_strategy)
bt.run()
bt.save_metrics(f"{data_dir}/optimized_result.csv")
bt.plot(ticker, f"MA_{best_short}_{best_long}", start_date, end_date)

print(f"\n📈 Final Sharpe Ratio: {bt.sharpe_ratio:.4f}")
print(f"📊 Full metrics saved to {data_dir}/optimized_result.csv")