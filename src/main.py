from concurrent.futures import ThreadPoolExecutor
import time

from stock.stock import Stock

# TODO: Next steps for this are:
# - accept RSI BUY / SELL indicators to env variables if present
# - implement async io instead of thread pooling
# - extract the ticker, RSI BUY, RSI SELL, quantities/values and trade frequency to a config yaml or csv file &
# - modify this file to extract from config file and configuration bot accordingly
# - implement additional strategies (potentially as a stock.strategies class)
# - deploy as aws lambda function using IAC and gh actions (copy existing implementation from directfile if needed)

def process_ticker(ticker):
    stock = Stock(ticker)
    while True:
      stock.analyze_and_trade()
      time.sleep(60 * 60)

def main():
    # Read tickers from the file
    stocks = [line.rstrip().upper() for line in open("stocks.txt", "r")]
    
    # Use ThreadPoolExecutor to process tickers concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(process_ticker, stocks)

if __name__ == "__main__":
    main()
