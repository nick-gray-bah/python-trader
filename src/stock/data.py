from datetime import datetime, timedelta
import yfinance
import matplotlib.dates as mdates


class StockData:
    ticker = None
    start = None
    end = None
    dates = None
    closes = None
    highs = None
    lows = None
    opens = None
    volumes = None

    def __init__(self, ticker, start=None, end=None):
        self.ticker = str.upper(ticker)
        self.end = end if end else datetime.now()
        self.start = start if start else (self.end - timedelta(days=30))
        
        self.fetch_data(self.start, self.end)

    def fetch_data(self, start, end):
        print("Pulling data for " + self.ticker)
        bars = yfinance.download(self.ticker, start=start, end=end)

        if bars.empty:
            raise ValueError(f"No data returned for {self.ticker}")

        self.dates = [mdates.date2num(d) for d in bars.index]
        self.closes = bars['Close'][self.ticker]
        self.highs = bars['High'][self.ticker]
        self.lows = bars['Low'][self.ticker]
        self.opens = bars['Open'][self.ticker]
        self.volumes = bars['Volume'][self.ticker]
