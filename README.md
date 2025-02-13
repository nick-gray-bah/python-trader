# Python Trader

## OVERVIEW

This project automates stock trading decisions for a list of provided tickers and a selected stock trading strategy. Available strategies are listed below.

Designed for efficiency and scalability, this project enables users to automate their selected trading strategy for any combination of stocks, time horizons and buy/sell thresholds.

## Strategies

### RSI & MACD Strategy

A dual-indicator strategy based on the Relative Strength Index (RSI) and the Moving Average Convergence Divergence (MACD).

Strategy Overview:

- The RSI acts as the primary signal indicator, identifying potential overbought or oversold conditions.
- The MACD serves as a confirmation indicator, filtering and validating trade signals to reduce false entries.

### EMA Crossover and RSI Strategy

A dual-indicator strategy based on a short term Exponential Moving Average (EMA) crossing above the long term EMA, and a Bullish RSI signal.

Strategy Overview:

- The EMA crossover acts as the primary signal indicator, indicating a bullish price movement.
- The RSI acts as the confirmation indicator, indicating that the stock is bullish but not overbought or oversold.

## Key Features

- Dynamic buy, sell, or hold decisions based on strategy alignment.
- Configurable stock symbols and trade parameters.
- Stop-loss and take-profit support for risk management.

## Steps to Run the Project

1. Add tickers to stocks.txt that you wish to run the bot for.

2. **Set env variables for your alpaca trading account**

   - ALPACA_API_KEY=<your_alpaca_api_key>
   - ALPACA_SECRET_KEY=<your_alpaca_secret_key>
   - ALPACA_BASE_URL=<your_alpaca_base_url>

3. **Select from an available trading strategy and define BUY/SELL parameters**

    TODO: add the params for each available strategy

4. **Install Packages and run app**

   Install dependencies and run the app with the following commands:

   ```bash
    pip install -r requirements.txt

    python src/main.py
   ```
