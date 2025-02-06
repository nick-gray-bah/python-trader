import csv
from io import StringIO
import io
import sys
import requests
import pandas as pd
import numpy as np
import schedule
import time
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import ALPHA_API_KEY

# Function to fetch stock symbols (S&P 500, NASDAQ, NYSE)
base_url = 'https://www.alphavantage.co/query'


def fetch_all_stock_symbols():
    try:
        CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo'

        with requests.Session() as s:
            download = s.get(CSV_URL)

            if download.status_code != 200:
                raise Exception(f'Error fetching data: {download.status_code}')

            decoded_content = download.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(decoded_content))
            filtered_df = df[df['exchange'].isin(['NYSE', 'NASDAQ'])]['symbol']

            if filtered_df.empty:
                raise Exception(f'Error fetching data: no stock data returned')

            return filtered_df

            # save to csv
            # filtered_df.to_csv('stocks.csv', index=False)

    except Exception as e:
        print(f'Error fetching stock symbols: {e}')


def fetch_stock_data(symbol):
    try:
        response = requests.get(base_url, {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': ALPHA_API_KEY,
            'datatype': 'csv',
            'outputsize': 'compact',
        })

        if response.status_code != 200:
            raise Exception(f'Error fetching data: {response.status_code}')

        decoded_content = response.content.decode('utf-8')

        df = pd.read_csv(StringIO(decoded_content))

        if df.empty:
            raise Exception(f'Error fetching data: no stock data returned')

        return df

    except Exception as e:
        print(f'error {str(e)}')
        return None


def check_bullish_conditions(symbol):
    data = fetch_stock_data(symbol)
    if data is None or len(data) < 34:
        return None

    data['EMA_10'] = EMAIndicator(data['close'], 10).ema_indicator()
    data['EMA_34'] = EMAIndicator(data['close'], 34).ema_indicator()
    data['RSI'] = RSIIndicator(data['close'], 14).rsi()

    last_three = data.tail(3)

    # check that ema 10 > ema 34 for the last three trading sessions
    ema_condition = (last_three['EMA_10'] > last_three['EMA_34']).all()

    # Check RSI > 50 (positive momentum) for the last three trading sessions
    rsi_condition = last_three['RSI'].iloc[-1] > 50

    return symbol if ema_condition and rsi_condition else None


def scan_stocks():
    print('Running stock scanner...')
    stock_symbols = fetch_all_stock_symbols()
    bullish_stocks = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_stock = {executor.submit(
            check_bullish_conditions, symbol): symbol for symbol in stock_symbols}

        for future in as_completed(future_to_stock):
            result = future.result()
            if result:
                bullish_stocks.append(result)

    print('Bullish stocks:', bullish_stocks)


if __name__ == '__main__':
    scan_stocks()
