import unittest
from datetime import datetime
from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from unittest import mock
from bullets.data_source.data_source_fmp import FmpDataSource


@mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
class TestPortfolio(unittest.TestCase):

    RESOLUTION = Resolution.DAILY
    START_TIME = datetime(2020, 1, 1)
    END_TIME = datetime(2020, 1, 2)
    STARTING_BALANCE = 5000
    DATA_SOURCE = FmpDataSource("TOKEN_GOES_HERE")

    def test_strategy(self, mock_get_price):
        strategy = Strategy(resolution= self.RESOLUTION,
                            start_time=self.START_TIME,
                            end_time=self.END_TIME,
                            starting_balance=self.STARTING_BALANCE,
                            data_source=self.DATA_SOURCE)
        runner = Runner(strategy)
        runner.start()


if __name__ == '__main__':
    unittest.main()
