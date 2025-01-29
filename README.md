# Python Trading Bot

## Overview

This project provides a comprehensive solution for stock market analysis and automated trading. The key objectives of this project are to:

1. **Fetch historical stock price data** from reliable financial sources.
2. **Calculate major financial indicators** such as the Relative Strength Index (RSI), Moving Averages (MA), Moving Average Convergence Divergence (MACD), and more.
3. **Run an automated trading bot** that buys and sells stocks based on the calculated financial indicators and user-defined thresholds.

Designed for scalability, efficiency, and extensibility, this project empowers users to perform in-depth technical analysis and automate their trading strategies.

## Steps to Run the Project

1. Add tickers to stocks.txt that you wish to run the bot for.

2. **Set env variables for your alpaca trading account**

   - ALPACA_API_KEY=<your_alpaca_api_key>
   - ALPACA_SECRET_KEY=<your_alpaca_secret_key>
   - ALPACA_BASE_URL=<your_alpaca_base_url>

3. **Override RSI thresholds if desired**

    Default buy threshold is RSI < 30 
    Default sell signal is RSI > 70

    override these by setting values for env variables

    RSI_BUY_THRESHOLD=<the_rsi_at_which_you_want_to_buy>
    RSI_SELL_THRESHOLD=<the_rsi_at_which_you_want_to_sell>

    The bot uses MACD as the secondary indicator to confirm the trade strategy,
    this is calculated as:

    latest MACD > MACD signal line -> confirm buy
    
    latest MACD < MACD signal line -> confirm sell


4. **Install Packages and run app**

   Install dependencies and run the app with the following commands:

   ```bash
    pip install -r requirements.txt

    python src/main.py
   ```
