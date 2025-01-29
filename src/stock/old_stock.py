import datetime
import math
import yfinance
import traceback
import pandas
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
import matplotlib.dates as mdates
from tenacity import retry, wait_fixed, stop_after_attempt, RetryError

from alpaca_client import alpaca_client

class OldStock:
    ticker = None
    dates = None
    closes = None
    highs = None
    lows = None
    opens = None
    volumes = None

    def __init__(self, ticker, start, end=datetime.datetime.now()):
        self.ticker = str.upper(ticker)
        self.fetch_data(start, end)

    def fetch_data(self, start, end):
        print("Pulling data for " + self.ticker)
        bars = yfinance.download(self.ticker, start=start, end=end)

        if bars.empty:
            raise ValueError(f"No data returned for {self.ticker}")

        self.dates = [mdates.date2num(d) for d in bars.index]
        self.closes = bars['Close'][self.ticker]
        self.highs = bars['High'][self.ticker]
        self.lows = bars['Low'][self.ticker]
        self.opens = bars['Open'][self.ticker]
        self.volumes = bars['Volume'][self.ticker]
        
    # INDICATORS

    def RSI(self, prices=None, window=14):
        values = self.validate_inputs(prices, window)
        return RSIIndicator(values, window=window)

    def MACD(self, prices=None, slow=26, fast=12, sign=9):
        values = self.validate_inputs(prices, slow)
        return MACD(values, window_slow=slow,
                    window_fast=fast, window_sign=sign)

    def SMA(self, period, prices=None):
        values = self.validate_inputs(prices, period)
        return SMAIndicator(values, window=period).sma_indicator()

    def EMA(self, period, prices=None):
        values = self.validate_inputs(prices, period)
        return EMAIndicator(values, period).ema_indicator()

    def validate_inputs(self, prices, period=None):
        values = prices if prices is not None else self.closes
        if period is not None and period > len(values):
            raise ValueError(
                "Period cannot be greater than the number of data points.")
        return pandas.Series(values)

  ### BUY SELL SIGNALS

    def generate_signal(self, RSI_Buy=30, RSI_Sell=70):
        """'BUY' when RSI is oversold(< RSI_Buy) and MACD crosses above the signal line

        'SELL' when RSI is overbought(> RSI_Sell) and MACD crosses below the signal line

        'HOLD' when no clear buy or sell condition exists

        Args:
            RSI_Buy (int, optional): The lower limit RSI (Buy if RSI < RSI_Buy). Defaults to 30.
            RSI_Sell (int, optional): The upper limit RSI (Sell if RSI > RSI_Sell). Defaults to 70.
        """
        latest_rsi = self.RSI().rsi().iloc[-1]
        latest_macd = self.MACD().macd().iloc[-1]
        latest_macd_signal = self.MACD().macd_signal().iloc[-1]

        if latest_rsi < RSI_Buy and latest_macd > latest_macd_signal:
            return "BUY"
        elif latest_rsi > RSI_Sell and latest_macd < latest_macd_signal:
            return "SELL"
        return "HOLD"
      
  
    #### ALPACA TRADE API FUNCTIONS
    
    def get_latest_price(self):
      """ gets the most recent quoted share price """
      try:
          quote = alpaca_client.get_latest_quote(self.ticker)

          if quote.ap is None:
              raise ValueError(
                  f'Failed to retrieve latest price for {self.ticker}')

          return quote.ap

      except Exception as e:
          print({"status": "Error", "error": str(e)})
      
    def calculate_trade_quantity(self, quantity, value):
      """ determines the number of shares to buy/sell
      Parameters:
          quantity (int): The quantity of the asset to sell. (If included value will be ignored)
          value (float): The value in USD to sell. (If included quantity will be calculated based on latest price)
      Returns:
          int: number of shares
      """
      if quantity is not None:
          return quantity
      elif value is not None:
          return math.floor(value / self.get_latest_price(value))
      else:
          raise ValueError(
              'must include value or quantity in buy orders')

    def submit_buy_order(self, quantity=None, value=None, stop_loss_percentage=None, take_profit_percentage=None):
        """ Executes a buy trade
        Parameters:
            quantity (int): The quantity of the asset to buy. (If included value will be ignored)
            value (float): The value in USD to buy. (If included quantity will be calculated based on latest price)
            stop_loss_percentage (float): The % of the order price to place stop loss order at
            take_profit_percentage (float): The % of the order price to place take profit order at
        """

        try:
            quantity = self.calculate_trade_quantity(quantity, value)

            # execute the buy order
            order = alpaca_client.submit_order(
                symbol=self.ticker,
                side='buy',
                qty=quantity,
                type='market',
                time_in_force='gtc',
            )

            print(f"Buy order {order.id} submitted for {self.ticker}")
            print(order)

            try:
                entry_price = self.check_order_status(order.id)
                print(f"""Buy order {order.id} filled for {
                      self.ticker} at ${entry_price}""")

                # Place stop loss or take profit if specified
                if stop_loss_percentage is not None:
                    stop_loss_price = round(
                        entry_price * (1 - stop_loss_percentage), 2)
                    self.submit_stop_loss_order(quantity, stop_loss_price)

                if take_profit_percentage is not None:
                    take_profit_price = round(
                        entry_price * (1 - take_profit_percentage), 2)
                    self.submit_take_profit_order(quantity, take_profit_price)

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print({"status": "Error", "error": str(e)})
            traceback.print_exc()

    def submit_sell_order(self, quantity=None, value=None):
        """ Executes a sell trade
        Parameters:
            quantity (int): The quantity of the asset to sell. (If included value will be ignored)
            value (float): The value in USD to sell. (If included quantity will be calculated based on latest price)
        """

        try:
            quantity = self.calculate_trade_quantity(quantity, value)

            order = alpaca_client.submit_order(
                symbol=self.ticker,
                side='sell',
                qty=quantity,
                type='market',
                time_in_force='gtc'
            )

            print(f"Sell order {order.id} submitted for {self.ticker}")
            print(order)

            try:
                exit_price = self.check_order_status(order.id)
                print(f"""Sell order {order.id} filled for {
                      self.ticker} at ${exit_price}""")

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print({"status": "Error", "error": str(e)})

    def submit_stop_loss_order(self, qty, stop_loss_price):
        """Submit a stop loss order."""

        try:
            order = alpaca_client.submit_order(
                symbol=self.ticker,
                qty=qty,
                side='sell',
                type='stop_limit',
                stop_price=stop_loss_price,
                time_in_force='gtc',
            )
            print(f"""Stop loss order submitted for {
                  self.ticker} at {stop_loss_price}""")
            print(order)

            try:
                exit_price = self.check_order_status(order.id)
                print(f"""Stop loss order {order.id} confirmed for {
                      self.ticker} at ${exit_price}""")

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print({"status": "Error", "error": str(e)})

    def submit_take_profit_order(self, qty, take_profit_price):
        """Submit a take profit order"""

        try:
            order = alpaca_client.submit_order(
                symbol=self.ticker,
                qty=qty,
                side='sell',
                type='limit',
                limit_price=take_profit_price,
                time_in_force='gtc',
            )
            print(f"""Take profit order placed for
                  {self.ticker} at {take_profit_price}""")
            print(order)

            try:
                exit_price = self.check_order_status(order.id)
                print(f"""Take profit order {order.id} confirmed for {
                      self.ticker} at ${exit_price}""")

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print({"status": "Error", "error": str(e)})

    @retry(wait=wait_fixed(60 * 3), stop=stop_after_attempt(10), reraise=True)
    def check_order_status(self, order_id):
        """Check the order status and retry every 3 minutes if needed (10 retries max)"""

        print(f"Checking status of order: {order_id}")

        order_status = alpaca_client.get_order(order_id)

        if order_status.status == 'filled':
            return float(order_status.filled_avg_price)
        else:
            # Will trigger a retry
            raise Exception(f"order: {order_id} not filled yet.")
