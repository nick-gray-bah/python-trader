from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import pandas as pd
from stock.stock import Stock

# TODO: Next steps for this are:
# - extract the desired strategy and the buy/sell signal indicators to a config file and import for dynamic configuration
# - deploy as aws lambda function using IAC and gh actions
# - implement async io instead of thread pooling


def process_ticker(ticker):
    try:
        stock = Stock(ticker)
        # result = stock.macd_crossover()
        result = stock.ema_crossover_and_rsi()
        # result = stock.macd_and_rsi()

        if result['signal'] == 'BUY':
            stock.trade.submit_buy_order(10)
        elif result['signal'] == 'SELL':
            stock.trade.close_position()

        return result

    except Exception as e:
        print(e)
        return {
            'ticker': stock.ticker,
            'signal': 'HOLD'
        }


def main():
    stocks = pd.read_csv('data/russell_1000.csv', header=0)['Ticker'].head(250)
    # stocks = ['LBTYK', 'BSX', 'TWLO', 'ITCI', 'WEN']
    buys = []
    sells = []

    with ThreadPoolExecutor() as executor:
        future_to_stock = {executor.submit(
            process_ticker, symbol): symbol for symbol in stocks}

        for future in as_completed(future_to_stock):
            result = future.result()
            if result['signal'] == 'BUY':
                buys.append(result)
            elif result['signal'] == 'SELL':
                sells.append(result)

    print('buys: ')
    print(json.dumps(buys, indent=4))
    print('sells: ')
    print(json.dumps(sells, indent=4))


if __name__ == "__main__":
    main()
