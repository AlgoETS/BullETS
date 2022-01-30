import unittest

from bullets import logger
from bullets.utils.market_utils import *


class TestMarket(unittest.TestCase):
    def test_invalid_weekday_sub_daily_market_open(self):
        try:
            date = datetime(2019, 1, 16, 4, 30, 20)
            self.assertEqual(False, is_market_open(date, Resolution.MINUTE))
            logger.info("Invalid weekday sub daily market open test successful")
        finally:
            pass
        # Tests to do : valid weekday daily, valid weekday sub daily, Invalid weekend daily, Invalid weekend subdaily,
        #               days away (in same week), days away (separated by weekend), days away (separated by holiday),
