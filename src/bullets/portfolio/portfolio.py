from bullets.portfolio.holding import Holding
from bullets.portfolio.transaction import Transaction
import datetime


class Portfolio:
    def __init__(self, start_balance: float):
        """
        Initializes the required variables for the Portfolio

        Args:
            starting_balance (str): API key from FinancialModelPrep
        """
        self.balance = start_balance
        self.holdings = {}
        self.short_holdings = set()
        self.transactions = []

    def buy(self, ticker: str, order_size: float, price: float, timestamp):
        ticker = ticker.upper()
        # Get holding
        holding = self.holdings.get(ticker, Holding(ticker))

        # Add transaction
        self.transactions.append(Transaction(ticker, order_size, price, timestamp))

        order_price = price * - order_size

        short_savings = 0
        if ticker in self.short_holdings:
            short_savings = self.holdings[ticker].nb_shares * self.holdings[ticker].avg_price
        # Insufficient funds check
        if self.get_balance(timestamp) + order_price - short_savings < 0:
            raise ValueError("Insufficient Funds : " + ticker)
        self.balance = self.balance + order_price

        # Create or update holding
        try:
            holding.add_shares(order_size, price)
            if holding.nb_shares < 0:
                self.short_holdings.add(ticker)
            self.holdings[ticker] = holding
        except ZeroDivisionError:
            self.holdings.pop(ticker)
            self.short_holdings.discard(ticker)

    def sell(self, ticker: str, nb_shares: float, price: float, timestamp):
        self.buy(ticker, -nb_shares, price, timestamp)

    def get_balance(self, date):
        balance = self.balance
        for ticker in self.short_holdings:
            holding = self.holdings.get(ticker)
            balance = balance + holding.nb_shares * holding.avg_price + holding.nb_shares * holding.avg_price
        return balance


