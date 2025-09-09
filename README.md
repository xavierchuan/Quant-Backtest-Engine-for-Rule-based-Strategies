# 📈 Quant Backtest Engine

A modular and extensible backtesting engine for rule-based trading strategies, with batch testing, parameter optimization, and performance reporting. Designed for systematic strategy evaluation and quantitative finance research.

---

## 🚀 Features

- Modular strategy structure (e.g., Moving Average Crossover, Mean Reversion)
- CLI-based execution with batch run & grid scan support
- Parameter optimization using `scipy.optimize`
- Performance metrics: Sharpe Ratio, Max Drawdown, CAGR, Win/Loss Ratio
- Visual equity curves, heatmaps, and Markdown reports
- Clean data processing and auto fallback from local files
- Easy to extend and configure

---

## 📁 Project Structure

```
quant-backtest-engine/
├── data/                      # Local fallback data (e.g., AAPL.csv)
├── engine/                    # Core backtest engine & performance metrics
├── strategies/                # Strategy logic, grid scan, optimizer
├── utils/                     # Data cleaning utilities
├── notebooks/                 # (Optional) Jupyter demos
├── output/                    # Auto-generated plots & metrics
├── main.py                    # Main run script
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

---

## ⚙️ Installation

```bash
git clone https://github.com/xiaochuanformal-web/quant-backtest-engine.git
cd quant-backtest-engine
python -m venv .venv
source .venv/bin/activate   # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧠 Strategy Example

```python
class MovingAverageCrossStrategy:
    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_ma = data['Close'].rolling(window=self.short_window).mean()
        long_ma = data['Close'].rolling(window=self.long_window).mean()
        signals = pd.Series(0, index=data.index)
        signals[short_ma > long_ma] = 1
        signals[short_ma < long_ma] = -1
        return signals
```

---

## 🧪 Sample Commands

Run default strategy:
```bash
python main.py --strategy ma --ticker AAPL --start 2021-01-01 --end 2023-01-01
```

Run grid scan:
```bash
python strategies/strategy_grid_scan.py --strategy ma --ticker BTC-USD
```

Optimize parameters:
```bash
python strategies/strategy_param_optimizer.py --strategy ma --ticker ETH-USD
```

---

## 📊 Output Example

```
output/
└── AAPL/
    ├── plot_MA_10_100_2021-2023.png
    ├── metrics_summary.csv
    └── report.md
```

You can visualize performance, compare strategies, and track parameter sensitivity.

---

## ✅ Requirements

- Python 3.9+
- pandas, numpy, matplotlib
- scipy, click, yfinance

---

## 📌 To-Do / Ideas

- Add transaction cost / slippage models
- Add RSI / MACD / Bollinger strategies
- Add Streamlit dashboard for interactive UI
- Add config file support for batch workflows

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Xiaochuan Li**  
 
**GitHub**:  [https://github.com/xavierchuan](https://github.com/xavierchuan)
**Linkedin**:[ www.linkedin.com/in/xiaochuan-li-finance](https://www.linkedin.com/in/xiaochuan-li-finance/)

---
