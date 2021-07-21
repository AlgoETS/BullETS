import os
import unittest

from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from bullets.data_source.data_source_fmp import FmpDataSource
from datetime import datetime


class TestPortfolio(unittest.TestCase):
    RESOLUTION = Resolution.DAILY
    START_TIME = datetime(2019, 3, 5)
    END_TIME = datetime(2019, 4, 22)
    STARTING_BALANCE = 5000
    FMP_TOKEN = os.getenv("FMP_TOKEN")

    def test_strategy(self):
        strategy = TestStrategy(resolution=self.RESOLUTION,
                                start_time=self.START_TIME,
                                end_time=self.END_TIME,
                                starting_balance=self.STARTING_BALANCE,
                                data_source=FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))
        runner = Runner(strategy)
        runner.start()
        self.assertEqual(5000, strategy.portfolio.start_balance)
        self.assertEqual(5489.624975, strategy.portfolio.update_and_get_balance())
        self.assertEqual(120.71247499999933, strategy.portfolio.cash_balance)
        self.assertEqual(9.79, strategy.portfolio.get_percentage_profit())
        self.assertEqual(33, len(strategy.portfolio.transactions))

    def test_strategy_none_date(self):
        self.assertRaisesRegex(TypeError, "Invalid strategy date type", TestStrategy,
                               self.RESOLUTION, None, None, self.STARTING_BALANCE,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_strategy_invalid_date(self):
        self.assertRaisesRegex(ValueError, "Strategy start time has to be before end time", TestStrategy,
                               self.RESOLUTION, self.END_TIME, self.START_TIME, self.STARTING_BALANCE,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_strategy_none_resolution(self):
        self.assertRaisesRegex(TypeError, "Invalid strategy resolution type", TestStrategy,
                               None, self.START_TIME, self.END_TIME, self.STARTING_BALANCE,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_strategy_none_data_source(self):
        self.assertRaisesRegex(TypeError, "Invalid strategy data source type", TestStrategy,
                               self.RESOLUTION, self.START_TIME, self.END_TIME, self.STARTING_BALANCE, None)

    def test_strategy_invalid_balance(self):
        self.assertRaisesRegex(ValueError, "Strategy starting balance should be positive", TestStrategy,
                               self.RESOLUTION, self.START_TIME, self.END_TIME, self.STARTING_BALANCE * -1,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))


class TestStrategy(Strategy):

    def on_resolution(self):
        self.portfolio.market_order("AAPL", 5)


if __name__ == '__main__':
    unittest.main()
