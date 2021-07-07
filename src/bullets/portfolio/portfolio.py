from bullets.data_source.data_source_interface import DataSourceInterface
from bullets.portfolio.holding import Holding
from bullets.portfolio.transaction import Transaction
from bullets import logger


class Portfolio:

    def __init__(self, start_balance: float, data_source: DataSourceInterface):
        """
        Initializes the required variables for the Portfolio
        Args:
            start_balance (str): Balance of the portfolio
        """
        self.start_balance = start_balance
        self.cash_balance = start_balance
        self.holdings = {}
        self.transactions = []
        self.timestamp = None
        self.data_source = data_source

    def market_order(self, symbol: str, nb_shares: float):
        """
        Order a stock at market price
        Args:
            symbol: Symbol of the stock you want to buy
            nb_shares: Number of shares of the order
        Returns: The transaction. The status explains whether the transaction was successful
        """
        price = self.data_source.get_price(symbol)
        transaction = self.__validate_and_create_transaction__(symbol, nb_shares, price)
        self.transactions.append(transaction)
        if transaction.status == Transaction.STATUS_SUCCESSFUL:
            self.__put_holding__(symbol, nb_shares, price)
        return transaction

    def update_and_get_balance(self):
        """
        Updates the current prices of the holdings and returns the total balance of the portfolio
        Returns: Total balance of the portfolio
        """
        balance = self.cash_balance
        for holding in self.holdings.values():
            holding.current_price = self.data_source.get_price(holding.symbol)
            balance = balance + holding.nb_shares * holding.current_price
        return balance

    def get_percentage_profit(self):
        return round(self.update_and_get_balance() / self.start_balance * 100 - 100, 2)

    def __validate_and_create_transaction__(self, symbol: str, nb_shares: float, price: float):
        """
        Validates and creates a transaction
        Args:
            symbol: Symbol of the stock you want to buy
            nb_shares: Number of shares of the order
            price: Price per share
        Returns: Transaction with a successful or failed status
        """
        if price is None:
            status = Transaction.STATUS_FAILED_SYMBOL_NOT_FOUND
        else:
            if self.cash_balance >= nb_shares * price:
                self.cash_balance = self.cash_balance - nb_shares * price
                status = Transaction.STATUS_SUCCESSFUL
            else:
                status = Transaction.STATUS_FAILED_INSUFFICIENT_FUNDS
        return Transaction(symbol, nb_shares, price, self.timestamp, status)

    def __put_holding__(self, symbol: str, nb_shares: float, price: float):
        """
        Creates, updates or deletes a holding based on the number of shares
        Args:
            symbol: Symbol of the stock you want to buy
            nb_shares: Number of shares of the order
            price: Price per share
        """
        holding = self.holdings.get(symbol, Holding(symbol))
        nb_shares = holding.add_shares(nb_shares, price)
        if nb_shares == 0:
            self.holdings.pop(symbol)
        else:
            self.holdings[symbol] = holding
