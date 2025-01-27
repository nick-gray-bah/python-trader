# Project Title

## Overview

This project provides a robust solution for financial analysis and stock data retrieval. The main objective is to retrieve historical stock price data and perform technical analysis, such as calculating indicators like the Relative Strength Index (RSI), using multiple data sources. The program is designed to be efficient, scalable, and easily extensible for future improvements.

## Features

- Fetch historical stock data from reliable financial sources.
- Compute key financial indicators like RSI.
- Visualize stock data and indicators through charts and graphs.
- Support for importing and working with images (e.g., charts, stock symbols) stored locally in the `src/images` directory.

## Steps to run

1. install requirements

    `pip install -r requirements.txt`

2. add stock tickers you want to analyze to src/stocks.txt

3. run the app

  `cd src/ && python main.py`