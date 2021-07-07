import unittest
import datetime

from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from bullets.data_source.data_source_fmp import FmpDataSource


class TestPortfolio(unittest.TestCase):
    RESOLUTION = Resolution.DAILY
    START_TIME = datetime.datetime(2019, 3, 5)
    END_TIME = datetime.datetime(2019, 4, 22)
    STARTING_BALANCE = 5000
    FMP_TOKEN = "878bd792d690ec6591d21a52de0b6774"

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
        self.assertEqual(34, len(strategy.portfolio.transactions))


class TestStrategy(Strategy):

    def on_resolution(self):
        self.portfolio.market_order("AAPL", 5)


if __name__ == '__main__':
    unittest.main()
