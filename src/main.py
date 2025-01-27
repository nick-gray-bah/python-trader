#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
import matplotlib
from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock

matplotlib.rcParams.update({'font.size': 9})


def main():
    stocks = ['AAPL']
    # If stocks array is empty, pull stock list from stocks.txt file
    stocks = stocks if len(stocks) > 0 else [
        line.rstrip() for line in open("stocks.txt", "r")]

    # Time frame to pull historical data for days={number of days to pull}
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=30)

    # Array of moving averages you want to get
    MAarr = [20, 200]
    allData = []

    for ticker in stocks:

        try:
            data = []

            print("Pulling data for " + ticker)

            stock = Stock(ticker, start, end)

            # # Append data to array
            # data.append(ticker.upper())

            # data.append(stock.closes[-1])

            # for MA in MAarr:
            #     computedSMA = stock.SMA(period=MA)
            #     # print(computedSMA)
            #     data.append(computedSMA[-1])

            # currentRsi = float("{:.2f}".format(stock.rsi[-1]))

            # if currentRsi > 70:
            #     data.append(str(currentRsi) + " 🔥")
            # elif currentRsi < 30:
            #     data.append(str(currentRsi) + " 🧊")
            # else:
            #     data.append(currentRsi)

            # chartLink = "https://finance.yahoo.com/quote/" + ticker + "/chart?p=" + ticker

            # data.append(chartLink)

            # allData.append(data)

            # # Shows chart only if current RSI is greater than or less than 70 or 30 respectively
            # if currentRsi < 30 or currentRsi > 70:

            #     stock.graph(MAarr)

        except Exception as e:
            print('Error: ', str(e))

    # print(tabulate(allData, headers=flatten([
    #     'Stock', 'Price', [str(x) + " MA" for x in MAarr], "RSI", "chart"])))


if __name__ == "__main__":
    main()
