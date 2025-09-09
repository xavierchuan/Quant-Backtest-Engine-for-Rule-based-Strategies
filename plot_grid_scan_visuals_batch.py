# plot_grid_scan_visuals_batch.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 标的列表（应与 grid_scan 一致）
tickers = ['AAPL', 'TSLA', 'BTC-USD', 'ETH-USD']

# 📊 绘图函数 1：Sharpe Ratio 热力图
def plot_heatmap(df, output_path, ticker):
    pivot = df.pivot(index="Short Window", columns="Long Window", values="Sharpe Ratio")
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot, annot=True, cmap="YlGnBu", fmt=".2f", center=0)
    plt.title(f"{ticker} - Sharpe Ratio Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "sharpe_ratio_heatmap.png"))
    plt.close()

# 📊 绘图函数 2：Radar Chart
def plot_radar_chart(df, output_path):
    labels = ["Total Return", "Annualized Return", "Max Drawdown", "Sharpe Ratio"]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    top3 = df.sort_values("Sharpe Ratio", ascending=False).head(3)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for idx, row in top3.iterrows():
        values = row[labels].tolist()
        values += values[:1]
        label = f"{int(row['Short Window'])}/{int(row['Long Window'])}"
        ax.plot(angles, values, label=label)
        ax.fill(angles, values, alpha=0.1)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Top 3 Strategies by Sharpe Ratio")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "top3_sharpe_radar.png"))
    plt.close()

# 📊 绘图函数 3：Bar Charts
def plot_bar_charts(df, output_path):
    # Top 5 by Annualized Return
    top5 = df.sort_values("Annualized Return", ascending=False).head(5)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=top5, x="Annualized Return", y=top5.apply(lambda r: f"{int(r['Short Window'])}/{int(r['Long Window'])}", axis=1), palette="Blues_d")
    plt.title("Top 5 Annualized Return")
    plt.xlabel("Annualized Return")
    plt.ylabel("Strategy (Short/Long)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "top5_annualized_return.png"))
    plt.close()

    # Top 5 by Lowest Max Drawdown
    best_dd = df.sort_values("Max Drawdown", ascending=True).head(5)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=best_dd, x="Max Drawdown", y=best_dd.apply(lambda r: f"{int(r['Short Window'])}/{int(r['Long Window'])}", axis=1), palette="Reds_r")
    plt.title("Top 5 Lowest Max Drawdown")
    plt.xlabel("Max Drawdown")
    plt.ylabel("Strategy (Short/Long)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "top5_drawdown.png"))
    plt.close()

# 🔁 主流程
for ticker in tickers:
    print(f"📊 Generating plots for {ticker}...")

    result_path = f"output/{ticker}/grid_scan_results.csv"
    figure_path = f"output/{ticker}/figures"
    os.makedirs(figure_path, exist_ok=True)

    # 读取回测结果
    df = pd.read_csv(result_path)

    # 分别绘图
    plot_heatmap(df, figure_path, ticker)
    plot_radar_chart(df, figure_path)
    plot_bar_charts(df, figure_path)

    print(f"✅ {ticker} 图像已生成于 {figure_path}/")