import unittest
import datetime

from src.bullets.portfolio import Portfolio


class TestPortfolio(unittest.TestCase):

    def test_buy_long(self):
        portfolio = Portfolio(1000)
        portfolio.buy("AAPL", 1000, 1, datetime.datetime.now())
        self.assertEqual(portfolio.cash, 0)
        portfolio.sell("AAPL", 1000, 2, datetime.datetime.now())
        self.assertEqual(portfolio.cash, 2000)
        self.assertEqual(0, len(portfolio.holdings))
        self.assertEqual(2, len(portfolio.transactions))

    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            Portfolio(1).buy("AAPL", 1000, 1, datetime.datetime.now())


if __name__ == '__main__':
    unittest.main()
