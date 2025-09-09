# utils/clean_data.py

import pandas as pd

def clean_data(data):
    """
    清洗 yfinance 返回的多层列数据：
    - 如果是 MultiIndex，则选择一个 ticker 并转换为扁平结构
    - 丢弃 NaN 行
    """
    # 如果是 MultiIndex（例如 ('Close', 'AAPL') 这种格式）
    if isinstance(data.columns, pd.MultiIndex):
        print("🔍 Raw columns:", data.columns)
        
        # 只保留单一 ticker（例如 'AAPL'）
        tickers = data.columns.levels[1].tolist()
        if len(tickers) > 1:
            raise ValueError(f"Data contains multiple tickers: {tickers}. Only single ticker is supported.")
        ticker = tickers[0]

        # 选出该 ticker 下的数据，并扁平化列名
        data = data.xs(ticker, level=1, axis=1)
        data.columns.name = None

        print("✅ Flattened columns:", data.columns)

    # 丢弃缺失值
    data.dropna(inplace=True)

    return data