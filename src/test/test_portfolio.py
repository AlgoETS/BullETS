import unittest
import datetime
from unittest import mock
from bullets.portfolio.portfolio import Portfolio
from bullets.portfolio.transaction import Transaction
from bullets.data_source.data_source_interface import DataSourceInterface


@mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
class TestPortfolio(unittest.TestCase):
    TIME = datetime.datetime(2021, 3, 10)

    def test_buy_sell_long(self, mock_get_price):
        portfolio = Portfolio(1000, DataSourceInterface())
        transaction = portfolio.market_order("AAPL", 1000)
        self.assertEqual(Transaction.STATUS_SUCCESSFUL, transaction.status)
        self.assertEqual(0, portfolio.cash_balance)
        transaction = portfolio.market_order("AAPL", -1000)
        self.assertEqual(Transaction.STATUS_SUCCESSFUL, transaction.status)
        self.assertEqual(1000, portfolio.cash_balance)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    def test_buy_sell_short(self, mock_get_price):
        portfolio = Portfolio(1000, DataSourceInterface())
        transaction = portfolio.market_order("AAPL", -1000)
        self.assertEqual(Transaction.STATUS_SUCCESSFUL, transaction.status)
        self.assertEqual(2000, portfolio.cash_balance)
        transaction = portfolio.market_order("AAPL", 1000)
        self.assertEqual(Transaction.STATUS_SUCCESSFUL, transaction.status)
        self.assertEqual(1000, portfolio.cash_balance)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    def test_insufficient_funds(self, mock_get_price):
        portfolio = Portfolio(1000, DataSourceInterface())
        transaction = portfolio.market_order("AAPL", 2000)
        self.assertEqual(Transaction.STATUS_FAILED_INSUFFICIENT_FUNDS, transaction.status)
        self.assertEqual(1000, portfolio.cash_balance)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(1, len(portfolio.transactions))

if __name__ == '__main__':
    unittest.main()
