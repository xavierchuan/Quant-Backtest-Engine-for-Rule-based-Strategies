# strategies/mean_reversion.py

import pandas as pd

class MeanReversionStrategy:
    def __init__(self, window=20, threshold=0.02):
        self.window = window
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # 假设 data 是一个 DataFrame，包含一列 'Close'
        close = data['Close']
        rolling_mean = close.rolling(window=self.window).mean()
        deviation = (close - rolling_mean) / rolling_mean

        signals = pd.Series(0, index=close.index)
        signals[deviation < -self.threshold] = 1   # Buy signal
        signals[deviation > self.threshold] = -1   # Sell signal

        return signals