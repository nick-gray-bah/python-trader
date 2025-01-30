import pandas
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator

class StockAnalysis:
    def __init__(self, ticker):
        self.ticker = str.upper(ticker)

    def RSI(self, prices, window=14):
        values = self._validate_inputs(prices, window)
        return RSIIndicator(values, window=window)

    def MACD(self, prices, slow=26, fast=12, sign=9):
        values = self._validate_inputs(prices, slow)
        return MACD(values, window_slow=slow,
                    window_fast=fast, window_sign=sign)

    def SMA(self, prices, period=20):
        values = self._validate_inputs(prices, period)
        return SMAIndicator(values, window=period).sma_indicator()

    def EMA(self, prices, period=20):
        values = self._validate_inputs(prices, period)
        return EMAIndicator(values, period).ema_indicator()

    def _validate_inputs(self, prices, period):
        if period > len(prices):
            raise ValueError(
                "Period cannot be greater than the number of data points.")

        return pandas.Series(prices)
