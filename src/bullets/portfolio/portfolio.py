from bullets.portfolio.holding import Holding
from bullets.portfolio.transaction import Transaction


class Portfolio:
    def __init__(self, starting_cash: float):
        """
        Initializes the required variables for the Portfolio

        Args:
            starting_cash (str): API key from FinancialModelPrep
        """
        self.cash = starting_cash
        self.holdings = {}
        self.transactions = []

    def buy(self, ticker: str, order_size: float, price: float, timestamp):
        ticker = ticker.upper()
        # Get holding
        holding = self.holdings.get(ticker, Holding(ticker))
        # Add transaction
        self.transactions.append(Transaction(ticker, order_size, price, timestamp))

        order_price = self.calculate_order_price(order_size, price)

        # Insufficient funds check
        if self.cash + order_price < 0:
            raise ValueError("Insufficient Funds : " + ticker)
        self.cash = self.cash + order_price

        # Create or update holding
        try:
            holding.add_shares(order_size, price)
            self.holdings[ticker] = holding
        except ZeroDivisionError:
            self.holdings.pop(ticker)

    def sell(self, ticker: str, nb_shares: float, price: float, timestamp):
        self.buy(ticker, -nb_shares, price, timestamp)

    @staticmethod
    def calculate_order_price(ordered_shares: float, price: float):
        return price * -ordered_shares


