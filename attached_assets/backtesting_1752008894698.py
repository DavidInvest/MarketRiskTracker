import pandas as pd
import numpy as np

class Backtester:
    def __init__(self):
        np.random.seed(42)

    def simulate_backtest(self):
        returns = np.random.normal(loc=0.001, scale=0.02, size=252)
        cumulative = (1 + returns).cumprod()
        return cumulative