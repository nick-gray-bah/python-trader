from datetime import datetime, timedelta
import threading
import yfinance
import matplotlib.dates as mdates


class StockData:
    _lock = threading.Lock()  # Class-level lock for yfinance downloads
    _cache = {}

    def __init__(self, ticker, start=None, end=None):
        self.ticker = str.upper(ticker)
        self.end = end if end else datetime.now()
        self.start = start if start else (self.end - timedelta(days=365))
        self._fetch_data()

    def _fetch_data(self):
        cache_key = (self.ticker, self.start, self.end)

        with StockData._lock:
            if cache_key in StockData._cache:
                bars = StockData._cache[cache_key]
            else:
                print("Pulling data for " + self.ticker)
                bars = yfinance.download(
                    self.ticker,
                    start=self.start,
                    end=self.end,
                    multi_level_index=False
                )
                StockData._cache[cache_key] = bars

        if bars.empty:
            raise ValueError(f"No data returned for {self.ticker}")

        self.dates = [mdates.date2num(d) for d in bars.index]
        self.closes = bars['Close']
        self.highs = bars['High']
        self.lows = bars['Low']
        self.opens = bars['Open']
        self.volumes = bars['Volume']
