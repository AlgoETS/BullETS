import unittest
import datetime
from bullets.portfolio import Portfolio


class TestPortfolio(unittest.TestCase):

    def test_buy_sell_long(self):
        portfolio = Portfolio(1000)
        portfolio.buy("AAPL", 1000, 1, datetime.datetime.now())
        self.assertEqual(0, portfolio.balance)
        portfolio.sell("AAPL", 1000, 2, datetime.datetime.now())
        self.assertEqual(2000, portfolio.balance)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    def test_buy_sell_short(self):
        portfolio = Portfolio(1000)
        portfolio.sell("AAPL", 1000, 1, datetime.datetime.now())
        self.assertEqual(0, portfolio.get_balance(None))
        portfolio.buy("AAPL", 1000, 1, datetime.datetime.now())
        self.assertEqual(1000, portfolio.get_balance(None))
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            Portfolio(1).buy("AAPL", 1000, 1, datetime.datetime.now())


if __name__ == '__main__':
    unittest.main()
