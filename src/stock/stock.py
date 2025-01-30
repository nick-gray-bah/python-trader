from stock.analysis import StockAnalysis
from stock.data import StockData
from stock.trade import StockTrade


class Stock:
    def __init__(self, ticker, start=None, end=None):
        self.ticker = str.upper(ticker)
        self.data = StockData(self.ticker, start, end)
        self.analysis = StockAnalysis(self.ticker)
        self.trade = StockTrade(self.ticker)

    def analyze_and_trade(self, RSI_Buy=30, RSI_Sell=70):
        """'BUY' when RSI is oversold(latest RSI < RSI_Buy) and MACD crosses above the signal line

        'SELL' when RSI is overbought(latest RSI > RSI_Sell) and MACD crosses below the signal line

        'HOLD' when no clear buy or sell condition exists

        Args:
            RSI_Buy (int, optional): The lower limit RSI (Buy if RSI < RSI_Buy). Defaults to 30.
            RSI_Sell (int, optional): The upper limit RSI (Sell if RSI > RSI_Sell). Defaults to 70.
        """

        prices = self.data.closes

        latest_rsi = self.analysis.rsi(prices).rsi().iloc[-1]
        macd = self.analysis.macd(prices)
        latest_macd = macd.macd().iloc[-1]
        latest_macd_signal = macd.macd_signal().iloc[-1]
        signal = 'HOLD'

        if latest_rsi < RSI_Buy and latest_macd > latest_macd_signal:
            signal = "BUY"
            # self.trade.submit_buy_order(quantity=10)
        elif latest_rsi > RSI_Sell and latest_macd < latest_macd_signal:
            signal = "SELL"
            # self.trade.submit_buy_order(quantity=10)

        indicators = {
            'ticker': self.ticker,
            'signal': signal,
            'latest_rsi': str(round(latest_rsi, 2)),
            'latest_macd': str(round(latest_macd, 2)),
            'latest_macd_signal': str(round(latest_macd_signal, 2)),
        }
        print(indicators)
