import pandas as pd

# 读取回测结果 CSV 文件
df = pd.read_csv("output/grid_scan_results.csv")

# 🎯 按 Sharpe Ratio 排序
sorted_by_sharpe = df.sort_values(by="Sharpe Ratio", ascending=False)

print("📈 Top 5 Strategies by Sharpe Ratio:\n")
print(sorted_by_sharpe.head())

# 💰 按 Annualized Return 排序
sorted_by_return = df.sort_values(by="Annualized Return", ascending=False)

print("\n💰 Top 5 Strategies by Annualized Return:\n")
print(sorted_by_return.head())

# 📉 按 Max Drawdown 排序（越小越好）
sorted_by_drawdown = df.sort_values(by="Max Drawdown", ascending=True)

print("\n📉 Top 5 Strategies with Lowest Max Drawdown:\n")
print(sorted_by_drawdown.head())