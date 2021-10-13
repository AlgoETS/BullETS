import unittest
from datetime import datetime
from unittest import mock

from bullets.data_indicators.indicators import Indicators
from bullets.data_source.data_source_interface import DataSourceInterface


class TestIndicators(unittest.TestCase):

    # @mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
    def test_sma(self, mock_get_price):
        indicateur = Indicators(DataSourceInterface())
        sma = Indicators.sma(symbol="TEST", target_date=datetime(2021, 1, 1), days=5)
        self.assertEqual(1, sma)

    # @mock.patch('bullets.data_source.data_source_interface.DataSourceInterface.get_price', return_value=1)
    def test_wma(self, mock_get_price):
        indicateur = Indicators(DataSourceInterface())
        wma = Indicators.wma(symbol="TEST", target_date=datetime(2021, 1, 1), days=5)
        self.assertEqual(1, wma)


if __name__ == '__main__':
    unittest.main()
