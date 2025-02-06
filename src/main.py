from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

from stock.stock import Stock

from scripts.bullish_conditions import fetch_all_stock_symbols

# TODO: Next steps for this are:
# - deploy as aws lambda function using IAC and gh actions
# - implement async io instead of thread pooling
# - modify this file to extract buy/sell signal indicators config file and configuration bot accordingly


def process_ticker(ticker):
    try:
        stock = Stock(ticker)
        result = stock.macd_and_rsi()
        # stock.macd_crossover()
        # stock.ema_crossover_and_rsi()
        return result

    except Exception as e:
        print(f'error: {e}')
        return {
            'ticker': stock.ticker,
            'signal': 'HOLD'
        }


def main():
    stocks = [line.rstrip().upper()
              for line in open("all_stocks.txt", "r")][100:200]
    buys = []
    sells = []

    # process multiple tickers concurrently
    with ThreadPoolExecutor() as executor:
        future_to_stock = {executor.submit(
            process_ticker, symbol): symbol for symbol in stocks}

        for future in as_completed(future_to_stock):
            result = future.result()
            if result['signal'] == 'BUY':
                buys.append(result['ticker'])
            elif result['signal'] == 'SELL':
                sells.append(result['ticker'])

    print('buys')
    print(buys)
    print('sells')
    print(sells)


if __name__ == "__main__":
    main()
