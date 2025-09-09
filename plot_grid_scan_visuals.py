# plot_grid_scan_visuals.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置风格
sns.set(style="whitegrid")

# 读取结果文件
df = pd.read_csv("output/grid_scan_results.csv")

# 创建输出图像目录
os.makedirs("output/figures", exist_ok=True)

### 🔥 1. Heatmap: Sharpe Ratio
pivot = df.pivot(index="Short Window", columns="Long Window", values="Sharpe Ratio")
plt.figure(figsize=(8, 6))
sns.heatmap(pivot, annot=True, cmap="YlGnBu", fmt=".2f", center=0)
plt.title("Grid Scan: Sharpe Ratio Heatmap")
plt.tight_layout()
plt.savefig("output/figures/sharpe_ratio_heatmap.png")
plt.close()

### 🔥 2. Radar Chart for Top 3 by Sharpe Ratio
def radar_chart(top_df, title, filename):
    labels = ["Total Return", "Annualized Return", "Max Drawdown", "Sharpe Ratio"]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for idx, row in top_df.iterrows():
        values = row[labels].tolist()
        values += values[:1]
        label = f"{int(row['Short Window'])}-{int(row['Long Window'])}"
        ax.plot(angles, values, label=label)
        ax.fill(angles, values, alpha=0.1)

    ax.set_title(title, y=1.08)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(f"output/figures/{filename}")
    plt.close()

# 获取 top 3 策略
top3_sharpe = df.sort_values(by="Sharpe Ratio", ascending=False).head(3)
radar_chart(top3_sharpe, "Top 3 Strategies by Sharpe Ratio", "top3_sharpe_radar.png")

### 🔥 3. Bar Plot: Annualized Return (Top 5)
top5_annual = df.sort_values("Annualized Return", ascending=False).head(5)
top5_annual["Strategy"] = top5_annual.apply(lambda r: f"{int(r['Short Window'])}-{int(r['Long Window'])}", axis=1)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=top5_annual,
    x="Annualized Return",
    y="Strategy",
    palette="Blues_d"
)
plt.title("Top 5 Strategies by Annualized Return")
plt.xlabel("Annualized Return")
plt.ylabel("Short-Long Window")
plt.tight_layout()
plt.savefig("output/figures/top5_annualized_return.png")
plt.close()

### 🔥 4. Bar Plot: Max Drawdown (Top 5 Lowest)
top5_drawdown = df.sort_values("Max Drawdown", ascending=True).head(5)
top5_drawdown["Strategy"] = top5_drawdown.apply(lambda r: f"{int(r['Short Window'])}-{int(r['Long Window'])}", axis=1)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=top5_drawdown,
    x="Max Drawdown",
    y="Strategy",
    palette="Reds_r"
)
plt.title("Top 5 Strategies with Lowest Max Drawdown")
plt.xlabel("Max Drawdown")
plt.ylabel("Short-Long Window")
plt.tight_layout()
plt.savefig("output/figures/top5_drawdown.png")
plt.close()

print("✅ 所有图像已生成并保存至 output/figures/")