import os
import unittest
import datetime
from unittest import mock
from bullets.portfolio.portfolio import Portfolio
from bullets.portfolio.transaction import Transaction, Status
from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets.data_source.data_source_fmp import FmpDataSource


class TestPortfolio(unittest.TestCase):
    TIME = datetime.datetime(2021, 3, 10)

    @mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
    @mock.patch('bullets.portfolio.portfolio.Portfolio._get_slippage_price', return_value=1)
    def test_buy_sell_long(self, mock_get_price, mock__get_slippage_price):
        portfolio = Portfolio(1000, DataSourceInterface(), 25, 1)
        transaction = portfolio.market_order("AAPL", 999)
        self.assertEqual(Status.SUCCESSFUL, transaction.status)
        self.assertEqual(0, portfolio.cash_balance)
        transaction = portfolio.market_order("AAPL", -999)
        self.assertEqual(Status.SUCCESSFUL, transaction.status)
        self.assertEqual(998, portfolio.cash_balance)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    @mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
    @mock.patch('bullets.portfolio.portfolio.Portfolio._get_slippage_price', return_value=1)
    def test_buy_sell_short(self, mock_get_price, mock__get_slippage_price):
        portfolio = Portfolio(1000, DataSourceInterface(), 25, 1)
        transaction = portfolio.market_order("AAPL", -1000)
        self.assertEqual(Status.SUCCESSFUL, transaction.status)
        self.assertEqual(1999, portfolio.cash_balance)
        transaction = portfolio.market_order("AAPL", 1000)
        self.assertEqual(Status.SUCCESSFUL, transaction.status)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    @mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
    @mock.patch('bullets.portfolio.portfolio.Portfolio._get_slippage_price', return_value=1)
    def test_insufficient_funds(self, mock_get_price, mock__get_slippage_price):
        portfolio = Portfolio(1000, DataSourceInterface(), 25, 1)
        transaction = portfolio.market_order("AAPL", 2000)
        self.assertEqual(Status.FAILED_INSUFFICIENT_FUNDS, transaction.status)
        self.assertEqual(1000, portfolio.cash_balance)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(1, len(portfolio.transactions))

    def test_market_order(self):
        data_source = FmpDataSource(os.getenv("FMP_TOKEN"), Resolution.MINUTE)
        portfolio = Portfolio(1000, data_source, 25, 1)
        portfolio.timestamp = datetime.datetime(2019, 3, 12, 15, 57)
        data_source.timestamp = datetime.datetime(2019, 3, 12, 15, 57)
        portfolio.market_order('AAPL', 5)
        data_source.timestamp = datetime.datetime(2019, 3, 13, 15, 57)
        portfolio.timestamp = datetime.datetime(2019, 3, 13, 15, 57)
        self.assertEqual(1003.8499999999999, portfolio.update_and_get_balance())

    def test_buy_stop_order(self):
        data_source = FmpDataSource(os.getenv("FMP_TOKEN"), Resolution.MINUTE)
        portfolio = Portfolio(1000, data_source, 25, 1)
        data_source.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.buy_stop_order("AAPL", 5, 131)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(1000, portfolio.update_and_get_balance())
        data_source.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(999.0, portfolio.update_and_get_balance())

    def test_sell_stop_order(self):
        data_source = FmpDataSource(os.getenv("FMP_TOKEN"), Resolution.MINUTE)
        portfolio = Portfolio(1000, data_source, 25, 1)
        data_source.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.sell_stop_order("AAPL", 5, 131)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(1000, portfolio.update_and_get_balance())
        data_source.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(999.0, portfolio.update_and_get_balance())

    def test_buy_limit_order(self):
        data_source = FmpDataSource(os.getenv("FMP_TOKEN"), Resolution.MINUTE)
        portfolio = Portfolio(1000, data_source, 25, 1)
        data_source.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.buy_limit_order("AAPL", 5, 131)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(1000, portfolio.update_and_get_balance())
        data_source.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(999.0, portfolio.update_and_get_balance())

    def test_sell_limit_order(self):
        data_source = FmpDataSource(os.getenv("FMP_TOKEN"), Resolution.MINUTE)
        portfolio = Portfolio(1000, data_source, 25, 1)
        data_source.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 6, 14, 15, 57)
        portfolio.sell_limit_order("AAPL", 5, 131)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(1000, portfolio.update_and_get_balance())
        data_source.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.timestamp = datetime.datetime(2021, 4, 14, 15, 57)
        portfolio.on_resolution()
        price = data_source.get_price('AAPL')
        self.assertEqual(999.0, portfolio.update_and_get_balance())

if __name__ == '__main__':
    unittest.main()
