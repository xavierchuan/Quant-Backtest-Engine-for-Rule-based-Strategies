# plot_grid_scan.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 加载结果
df = pd.read_csv("output/grid_scan_results.csv")

# 将参数转换为字符串以便分组热力图
df['Short Window'] = df['Short Window'].astype(str)
df['Long Window'] = df['Long Window'].astype(str)

# 设置 Seaborn 样式
sns.set(style="whitegrid")

# 想要展示的所有指标
metrics = ['Sharpe Ratio', 'Annualized Return', 'Max Drawdown', 'Total Return']

# 创建图表目录
os.makedirs("output/plots", exist_ok=True)

# 遍历每个指标生成热力图
for metric in metrics:
    pivot = df.pivot(index="Short Window", columns="Long Window", values=metric)

    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(
        pivot, annot=True, fmt=".2f", cmap="YlGnBu",
        linewidths=0.5, cbar_kws={'label': metric}
    )
    plt.title(f"Grid Scan: {metric} Heatmap", fontsize=14)
    plt.xlabel("Long Window")
    plt.ylabel("Short Window")
    plt.tight_layout()

    # 保存图表
    filename = f"output/plots/grid_heatmap_{metric.lower().replace(' ', '_')}.png"
    plt.savefig(filename)
    print(f"✅ Saved: {filename}")

    plt.close()