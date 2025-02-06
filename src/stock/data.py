from datetime import datetime, timedelta
import threading
import yfinance


class StockData:
    _lock = threading.Lock()  # Class-level lock for yfinance downloads to support multithreading
    _cache = {}

    def __init__(self, ticker):
        self.ticker = str.upper(ticker)

    def fetch_bars(self, interval='1D', timeframe=120):
        end = datetime.now()
        start = end - timedelta(days=timeframe)
        cache_key = (self.ticker, start, end, interval, timeframe)

        if cache_key in StockData._cache:
            return StockData._cache[cache_key]

        with StockData._lock:
            print("Pulling data for " + self.ticker)
            try:
                bars = yfinance.download(
                    self.ticker,
                    start=start,
                    end=end,
                    interval=interval,
                    multi_level_index=False
                )

                if bars.empty:
                    self.remove_ticker()
                    raise ValueError(f"no data returned for {self.ticker}")

                StockData._cache[cache_key] = bars
                return bars

            except Exception as e:
                print(f'error fetching bars: {e}')

    def remove_ticker(self):
      print(f'removing ticker {self.ticker} from all_stock.txt')
      
      with open('all_stocks.txt', "r") as file:
        symbols = file.read().splitlines()
        updated_symbols = [symbol for symbol in symbols if symbol != self.ticker]
        
      with open('all_stocks.txt', "w") as file:
        for symbol in updated_symbols:
            file.write(symbol + "\n")