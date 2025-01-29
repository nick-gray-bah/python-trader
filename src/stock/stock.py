from stock.analysis import StockAnalysis
from stock.data import StockData
from stock.trade import StockTrade


class Stock:
    ticker = None
    data = None
    analysis = None
    trade = None

    def __init__(self, ticker, start=None, end=None):
        self.ticker = str.upper(ticker)
        self.data = StockData(self.ticker, start, end)
        self.analysis = StockAnalysis(self.ticker, data=self.data)
        self.trade = StockTrade(self.ticker)

    def generate_signal(self, RSI_Buy=30, RSI_Sell=70):
        """'BUY' when RSI is oversold(latest RSI < RSI_Buy) and MACD crosses above the signal line

        'SELL' when RSI is overbought(latest RSI > RSI_Sell) and MACD crosses below the signal line

        'HOLD' when no clear buy or sell condition exists

        Args:
            RSI_Buy (int, optional): The lower limit RSI (Buy if RSI < RSI_Buy). Defaults to 30.
            RSI_Sell (int, optional): The upper limit RSI (Sell if RSI > RSI_Sell). Defaults to 70.
        """
        latest_rsi = self.analysis.RSI().rsi().iloc[-1]
        latest_macd = self.analysis.MACD().macd().iloc[-1]
        latest_macd_signal = self.analysis.MACD().macd_signal().iloc[-1]

        if latest_rsi < RSI_Buy and latest_macd > latest_macd_signal:
            return "BUY"
        elif latest_rsi > RSI_Sell and latest_macd < latest_macd_signal:
            return "SELL"
        return "HOLD"
