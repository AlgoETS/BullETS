import unittest
from datetime import datetime
from bullets.strategy import Strategy
from bullets.runner import Runner
from bullets.data_source.base import BaseData


class TestPortfolio(unittest.TestCase):

    def test_strategy(self):
        runner = Runner(BaseData(ticker="AAPL", start_time=datetime(2020,1,1), end_time=datetime(2020,1,2), client=None))
        strategy = Strategy(start_time=datetime(2020,1,1), end_time=datetime(2020,1,2), starting_balance=5000,
                            runner=runner, ticker="AAPL")
        runner.attach(strategy)
        runner.start()


if __name__ == '__main__':
    unittest.main()
