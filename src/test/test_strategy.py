import unittest
import datetime

from bullets.portfolio.portfolio import Portfolio
from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from unittest import mock
from bullets.data_source.data_source_fmp import FmpDataSource


class TestPortfolio(unittest.TestCase):

    RESOLUTION = Resolution.DAILY
    START_TIME = datetime.datetime(2020, 1, 1)
    END_TIME = datetime.datetime(2020, 1, 2)
    STARTING_BALANCE = 5000
    FMP_TOKEN = "TOKEN_GOES_HERE"

    @mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
    def test_strategy(self, mock_get_price):
        strategy = Strategy(resolution= self.RESOLUTION,
                            start_time=self.START_TIME,
                            end_time=self.END_TIME,
                            starting_balance=self.STARTING_BALANCE,
                            data_source=FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))
        runner = Runner(strategy)
        runner.start()


if __name__ == '__main__':
    unittest.main()
