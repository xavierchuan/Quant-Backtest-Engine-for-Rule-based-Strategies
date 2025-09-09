import pandas as pd

class MovingAverageCrossStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # 计算短期和长期移动平均线
        short_ma = data['Close'].rolling(window=self.short_window).mean()
        long_ma = data['Close'].rolling(window=self.long_window).mean()

        # 初始化信号为 0
        signals = pd.Series(0, index=data.index)

        # 生成信号：短期 > 长期 为 1，短期 < 长期 为 -1
        condition_long = short_ma > long_ma
        condition_short = short_ma < long_ma

        signals[condition_long] = 1
        signals[condition_short] = -1

        return signals