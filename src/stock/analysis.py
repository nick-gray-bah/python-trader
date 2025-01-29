import pandas
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator

class StockAnalysis:
    ticker = None
    data = None
    
    def __init__(self, ticker, data):
        self.ticker = str.upper(ticker)
        self.data = data

    def RSI(self, prices=None, window=14):
        values = self.validate_inputs(prices, window)
        return RSIIndicator(values, window=window)

    def MACD(self, prices=None, slow=26, fast=12, sign=9):
        values = self.validate_inputs(prices, slow)
        return MACD(values, window_slow=slow,
                    window_fast=fast, window_sign=sign)

    def SMA(self, period, prices=None):
        values = self.validate_inputs(prices, period)
        return SMAIndicator(values, window=period).sma_indicator()

    def EMA(self, period, prices=None):
        values = self.validate_inputs(prices, period)
        return EMAIndicator(values, period).ema_indicator()

    def validate_inputs(self, prices, period=None):
        values = prices if prices is not None else self.data.closes
        if period is not None and period > len(values):
            raise ValueError(
                "Period cannot be greater than the number of data points.")
        return pandas.Series(values)