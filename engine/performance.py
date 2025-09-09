# engine/performance.py

import numpy as np

class PerformanceEvaluator:
    def __init__(self, portfolio_values):
        self.portfolio_values = portfolio_values.dropna()
        self.returns = self.portfolio_values.pct_change().dropna()

    def total_return(self):
        return (self.portfolio_values.iloc[-1] / self.portfolio_values.iloc[0]) - 1

    def annualized_return(self):
        total_ret = self.total_return()
        num_days = len(self.portfolio_values)
        return (1 + total_ret) ** (252 / num_days) - 1

    def max_drawdown(self):
        cumulative = self.portfolio_values.cummax()
        drawdowns = self.portfolio_values / cumulative - 1
        return drawdowns.min()

    def sharpe_ratio(self, risk_free_rate=0.01):
        excess_return = self.returns - (risk_free_rate / 252)
        return np.sqrt(252) * excess_return.mean() / excess_return.std()