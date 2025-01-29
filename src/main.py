from datetime import datetime, timedelta, timezone
import traceback

from stock.stock import Stock

def main():
    stocks = ['QQQ']

    # If stocks array is empty, pull stock list from stocks.txt file
    stocks = stocks if len(stocks) > 0 else [
        line.rstrip().upper() for line in open("stocks.txt", "r")
    ]

    # Time frame to pull historical data
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=365)

    for ticker in stocks:
        try:
          
            # TODO: Next steps for this are:
            # - accept RSI BUY / SELL indicators to env variables if present
            # - extract the ticker, RSI BUY, RSI SELL, quantities/values and trade frequency to a config yaml or csv file &
            # - modify this file to extract from config file and configuration bot accordingly
            # - implement additional strategies (potentially as a stock.strategies class)
            # - deploy as aws lambda function using IAC and gh actions (copy existing implementation from directfile if needed)
            
            stock = Stock(ticker, start, end)
            signal = stock.generate_signal()
            
            newData = []
            
            print(f'Stock: {stock.ticker} Signal: {signal}')
        
            newData.append(stock.analysis.SMA(20))
            newData.append(stock.analysis.SMA(200))
            newData.append(stock.analysis.EMA(20))
            newData.append(stock.analysis.MACD().macd())
            newData.append(stock.analysis.MACD().macd_signal())
            newData.append(stock.analysis.RSI().rsi())
            print(newData)
            
            # stock.trade.submit_buy_order(10)
            # stock.trade.submit_sell_order(10)
            

        except Exception as e:
            print('Error: ', str(e))
            traceback.print_exc()


if __name__ == "__main__":
    main()
