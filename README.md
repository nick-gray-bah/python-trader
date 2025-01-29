# Python Trader

## RSI & MACD Strategy

This application automates stock trading decisions using a dual-indicator strategy based on the Relative Strength Index (RSI) and the Moving Average Convergence Divergence (MACD).

Strategy Overview:

The RSI acts as the primary signal indicator, identifying potential overbought or oversold conditions.
The MACD serves as a confirmation indicator, filtering and validating trade signals to reduce false entries.

## Key Features:

   - Dynamic buy, sell, or hold decisions based on RSI-MACD alignment.
   - Configurable stock symbols and trade parameters.
   - Stop-loss and take-profit support for risk management.

Designed for efficiency and scalability, this project enables users to perform highspeed analysis and automation of the RSI-MACD trading strategy againest any number of stocks.

## Steps to Run the Project

1. Add tickers to stocks.txt that you wish to run the bot for.

2. **Set env variables for your alpaca trading account**

   - ALPACA_API_KEY=<your_alpaca_api_key>
   - ALPACA_SECRET_KEY=<your_alpaca_secret_key>
   - ALPACA_BASE_URL=<your_alpaca_base_url>

3. **Override RSI thresholds if desired**

   defaults:
    - latest RSI < 30  -> signal buy
    - latest RSI > 70 -> signal sell

    Override these by setting values for env variables:

    - RSI_BUY_THRESHOLD=<the_rsi_at_which_you_want_to_buy>
    - RSI_SELL_THRESHOLD=<the_rsi_at_which_you_want_to_sell>

    The bot uses MACD as the secondary indicator to confirm the trade strategy,
    this is calculated as:

    - latest MACD > MACD signal line -> confirm buy
    - latest MACD < MACD signal line -> confirm sell
  
   These cannot currently be modified, but changes are coming to allow different
   strategies other than MACD as the confirmation signal.


5. **Install Packages and run app**

   Install dependencies and run the app with the following commands:

   ```bash
    pip install -r requirements.txt

    python src/main.py
   ```
