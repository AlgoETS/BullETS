from bullets.portfolio.holding import Holding
from bullets.portfolio.transaction import Transaction


class Portfolio:
    def __init__(self, start_balance: float):
        """
        Initializes the required variables for the Portfolio

        Args:
            start_balance (str): Balance of the portfolio
        """
        self.balance = start_balance
        self.holdings = {}
        self.short_holdings = set()
        self.transactions = []

    def buy(self, symbol: str, order_size: float, price: float, timestamp):
        symbol = symbol.upper()

        # Get holding else create a new one
        holding = self.holdings.get(symbol, Holding(symbol))

        # Add transaction
        self.transactions.append(Transaction(symbol, order_size, price, timestamp))

        # Calculate total price of the order
        order_price = price * order_size

        # Calculates money that is being held by the shorted stock
        short_savings = 0
        if symbol in self.short_holdings:
            short_savings = -(self.holdings[symbol].nb_shares * self.get_current_price(symbol, timestamp))

        # Insufficient funds check
        if self.get_balance(timestamp) - order_price + short_savings < 0:
            raise ValueError("Insufficient Funds : " + symbol)
        # Subtracts the price of the order from the balance
        self.balance = self.balance - order_price

        # Create or update holding
        try:
            # Tries to add shares to the holding
            holding.add_shares(order_size, price)
            # If the holding is short
            if holding.nb_shares < 0:
                # Add short holding to short list
                self.short_holdings.add(symbol)
            # Adds the holding to the list
            self.holdings[symbol] = holding
        # Catches ZeroDivisionError if there are no more shares for the stock
        except ZeroDivisionError:
            # Removes the holding
            self.holdings.pop(symbol)
            self.short_holdings.discard(symbol)

    def sell(self, symbol: str, nb_shares: float, price: float, timestamp):
        self.buy(symbol, -nb_shares, price, timestamp)

    def get_balance(self, date):
        balance = self.balance
        for symbol in self.short_holdings:
            holding = self.holdings.get(symbol)
            # Subtract current price of shares
            balance = balance + holding.nb_shares * self.get_current_price(holding.symbol, date)
        return balance

    # TODO Get current price from client
    def get_current_price(self, symbol, date):
        return 1
