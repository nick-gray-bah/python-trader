import math
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed
from alpaca_trade_api import REST

from config import ALPACA_API_KEY, ALPACA_BASE_URL, ALPACA_SECRET_KEY


class StockTrade:

    def __init__(self, ticker):
        self.ticker = ticker
        self.trade_history = []
        self.alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)

    def get_latest_price(self):
        """ gets the most recent quoted share price """
        try:
            quote = self.alpaca.get_latest_quote(self.ticker)

            if quote.ap is None:
                raise ValueError(
                    f'Failed to retrieve latest price for {self.ticker}')

            return quote.ap

        except Exception as e:
            print(e)

    def get_current_position(self):
        """ gets the quantity of shares currently held """
        try:
            position = self.alpaca.get_position(self.ticker)
            return int(position.qty)

        except Exception as e:
            print(e)
            return None

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
        """ Executes a buy trade if no stock is currently held
        Parameters:
            quantity (int): The quantity of the asset to buy. (If included value will be ignored)
            value (float): The value in USD to buy. (If included quantity will be calculated based on latest price)
            stop_loss_percentage (float): The % of the order price to place stop loss order at
            take_profit_percentage (float): The % of the order price to place take profit order at
        """

        try:
            position = self.get_current_position()

            if position is not None:
                print(f'{self.ticker} already owned, no order submitted')
                return

            quantity = self.calculate_trade_quantity(quantity, value)

            order = self.alpaca.submit_order(
                symbol=self.ticker,
                side='buy',
                qty=quantity,
                type='market',
                time_in_force='gtc',
            )

            print(f"Buy order {order.id} submitted for {self.ticker}")
            self.trade_history.append(order)

            try:
                entry_price = self.check_order_status(order.id)
                print(f"""Buy order {order.id} filled for {
                      self.ticker} at ${entry_price}""")

                # Place stop loss or take profit if included
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
            print(e)

    def close_position(self):
        """Liquidates the position at market price"""

        try:
            position = self.get_current_position()

            if position is None:
                return

            self.alpaca.close_position(self.ticker)

        except Exception as e:
            print(e)

    def submit_sell_order(self, quantity=None, value=None):
        """ Executes a sell trade
        Parameters:
            quantity (int): The quantity of the asset to sell. (If included value will be ignored)
            value (float): The value in USD to sell. (If included quantity will be calculated based on latest price)
        """

        try:
            quantity = self.calculate_trade_quantity(quantity, value)

            order = self.alpaca.submit_order(
                symbol=self.ticker,
                side='sell',
                qty=quantity,
                type='market',
                time_in_force='gtc'
            )

            print(f"Sell order {order.id} submitted for {self.ticker}")
            self.trade_history.append(order)

            try:
                exit_price = self.check_order_status(order.id)
                print(f"""Sell order {order.id} filled for {
                      self.ticker} at ${exit_price}""")

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print(e)

    def submit_stop_loss_order(self, quantity, stop_loss_price):
        """Submit a stop loss order."""

        try:
            order = self.alpaca.submit_order(
                symbol=self.ticker,
                qty=quantity,
                side='sell',
                type='stop_limit',
                stop_price=stop_loss_price,
                time_in_force='gtc',
            )
            print(f"""Stop loss order submitted for {
                  self.ticker} at {stop_loss_price}""")
            self.trade_history.append(order)

            try:
                exit_price = self.check_order_status(order.id)
                print(f"""Stop loss order {order.id} confirmed for {
                      self.ticker} at ${exit_price}""")

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print(e)

    def submit_take_profit_order(self, quantity, take_profit_price):
        """Submit a take profit order"""

        try:
            order = self.alpaca.submit_order(
                symbol=self.ticker,
                qty=quantity,
                side='sell',
                type='limit',
                limit_price=take_profit_price,
                time_in_force='gtc',
            )
            print(f"""Take profit order placed for
                  {self.ticker} at {take_profit_price}""")
            self.trade_history.append(order)

            try:
                exit_price = self.check_order_status(order.id)
                print(f"""Take profit order {order.id} confirmed for {
                      self.ticker} at ${exit_price}""")

            except RetryError:
                print(f"order: {order.id} could not be confirmed")

        except Exception as e:
            print(e)

    @retry(wait=wait_fixed(15), stop=stop_after_attempt(5), reraise=True)
    def check_order_status(self, order_id):
        """Check the order status and retry every 3 minutes if needed (10 retries max)"""

        print(f"Checking status of order: {order_id}")

        order_status = self.alpaca.get_order(order_id)

        if order_status.status == 'filled':
            return float(order_status.filled_avg_price)
        else:
            # Will trigger a retry
            raise Exception(f"order: {order_id} not filled yet.")