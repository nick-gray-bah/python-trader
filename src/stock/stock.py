from stock.data import StockData
from stock.trade import StockTrade

from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator


class Stock:
    def __init__(self, ticker):
        self.ticker = str.upper(ticker)
        self.data = StockData(self.ticker)
        self.trade = StockTrade(self.ticker)

    def ema_crossover_and_rsi(self, short_ema=10, long_ema=34, rsi_window=14, rsi_lower=50, rsi_upper=75):
        """
        'BUY' when short ema crosses over long ema at the last close and rsi > rsi_threshold
        'SELL'  when long ema crosses over short ema at the last close
        'HOLD' default
        """
        prices = self.data.fetch_bars()
        
        if prices is None or len(prices) < long_ema:
          raise ValueError(f"insufficient data for {self.ticker}")

        prices['ema_10'] = EMAIndicator(
            prices['Close'], short_ema).ema_indicator()
        prices['ema_34'] = EMAIndicator(
            prices['Close'], long_ema).ema_indicator()
        prices['RSI'] = RSIIndicator(prices['Close'], rsi_window).rsi()

        latest_ema_10 = prices['ema_10'].iloc[-1]
        prev_ema_10 = prices['ema_10'].iloc[-2]
        latest_ema_34 = prices['ema_34'].iloc[-1]
        prev_ema_34 = prices['ema_10'].iloc[-2]
        latest_rsi = prices['RSI'].iloc[-1]
        
        signal = 'HOLD'
        if latest_ema_10 >= latest_ema_34 and prev_ema_10 < prev_ema_34 and rsi_lower < latest_rsi < rsi_upper:
            signal = "BUY"
        elif latest_ema_34 >= latest_ema_10 and prev_ema_34 < prev_ema_10:
            signal = "SELL"

        results = {
            'ticker': self.ticker,
            'strategy': 'ema 10 / ema 34 crossover and RSI range',
            'signal': signal,
            'latest_ema_10': str(round(latest_ema_10, 2)),
            'prev_ema_10': str(round(prev_ema_10, 2)),
            'latest_ema_34': str(round(latest_ema_34, 2)),
            'prev_ema_34': str(round(prev_ema_34, 2)),
            'RSI': str(round(prices['RSI'].iloc[-1], 2))
        }

        return results

    def macd_crossover(self, window_slow=26, window_fast=12, window_sign=9):
        """ 
        'BUY' when macd crossed over signal line in the last close
        'SELL' when macd crossed under signal line in the last close
        'HOLD' default
        """
        prices = self.data.fetch_bars()

        if prices is None or len(prices) < window_slow + window_sign:
            raise ValueError(f"insufficient data for {self.ticker}")

        macd = MACD(prices['Close'], window_slow,
                    window_fast, window_sign)

        latest_macd = macd.macd().iloc[-1]
        prev_macd = macd.macd().iloc[-2]

        latest_macd_signal = macd.macd_signal().iloc[-1]
        prev_macd_signal = macd.macd_signal().iloc[-2]

        signal = 'HOLD'
        if latest_macd > latest_macd_signal and prev_macd < prev_macd_signal:
            signal = "BUY"
        elif latest_macd < latest_macd_signal and prev_macd > prev_macd_signal:
            signal = "SELL"

        result = {
            'ticker': self.ticker,
            'strategy': 'macd crossover',
            'signal': signal,
            'latest_macd': str(round(latest_macd, 2)),
            'latest_macd_signal': str(round(latest_macd_signal, 2))
        }
        
        return result

    def macd_and_rsi(self, rsi_buy=30, rsi_sell=70, window_slow=26, window_fast=12, window_sign=9):
        """
        'BUY' when RSI is oversold(latest RSI < RSI_Buy) and MACD is above the signal line
        'SELL' when RSI is overbought(latest RSI > RSI_Sell) and MACD is below the signal line
        'HOLD' default
        """
        prices = self.data.fetch_bars()

        if prices is None or prices.empty:
            raise ValueError(f"insufficient data for {self.ticker}")

        latest_rsi = RSIIndicator(prices['Close'], 14).rsi().iloc[-1]
        macd = MACD(prices['Close'], window_slow,
                    window_fast, window_sign)

        latest_macd = macd.macd().iloc[-1]
        latest_macd_signal = macd.macd_signal().iloc[-1]

        signal = 'HOLD'
        if latest_rsi < rsi_buy and latest_macd > latest_macd_signal:
            signal = "BUY"
        elif latest_rsi > rsi_sell and latest_macd < latest_macd_signal:
            signal = "SELL"

        result = {
            'ticker': self.ticker,
            'strategy': 'macd and rsi',
            'signal': signal,
            'latest_rsi': str(round(latest_rsi, 2)),
            'latest_macd': str(round(latest_macd, 2)),
            'latest_macd_signal': str(round(latest_macd_signal, 2)),
        }

        return result
