from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from stock.stock import Stock

# TODO: Next steps for this are:
# - extract the desired strategy and the buy/sell signal indicators to a config file and import for dynamic configuration
# - deploy as aws lambda function using IAC and gh actions
# - implement async io instead of thread pooling


def process_ticker(ticker):
    try:
        stock = Stock(ticker)
        result = stock.macd_crossover()
        # result = stock.ema_crossover_and_rsi(rsi_lower=30, rsi_upper=70)
        # result = stock.macd_and_rsi(RSI_Buy=43, RSI_Sell=80)

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
    stocks = [line.rstrip().upper()
              for line in open("data/all_stocks.txt", "r")]
  
    buys = []
    sells = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_stock = {executor.submit(
            process_ticker, ticker): ticker for ticker in stocks}

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
