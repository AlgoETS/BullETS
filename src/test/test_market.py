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

    def valid_weekday_daily_market_open(self):
        try:
            date = datetime(2022, 2, 1, 1, 30, 20)
            self.assertEqual(True, is_market_open(date, Resolution.DAILY))
            logger.info("Valid weekday daily market open test successful")
        finally:
            pass

    def test_valid_weekday_sub_daily_market_open(self):
        try:
            date = datetime(2019, 1, 16, 1, 30, 20)
            self.assertEqual(True, is_market_open(date, Resolution.MINUTE))
            logger.info("Valid weekday sub daily market open test successful")
        finally:
            pass

    def test_invalid_weekend_daily_market_open(self):
        try:
            date = datetime(202, 2, 5, 1, 30, 20)
            self.assertEqual(False, is_market_open(date, Resolution.DAILY))
            logger.info("Invalid weekend daily market open test successful")
        finally:
            pass

    def test_invalid_weekend_subdaily_market_open(self):
        try:
            date = datetime(202, 2, 5, 4, 30, 20)
            self.assertEqual(False, is_market_open(date, Resolution.MINUTE))
            logger.info("Invalid weekend subdaily market open test successful")
        finally:
            pass

    def test_days_away_same_week(self):
        try:
            startdate = datetime(2022, 1, 10)
            enddate = datetime(2022,1,14)
            daysaway = 4
            self.assertEqual(get_date_in_x_market_days_away(daysaway,startdate),enddate)
            logger.info("Return date 4 days away same week test successful")
        finally:
            pass

    def test_days_away_over_weekend(self):
        try:
            startdate = datetime(2022,1,10)
            enddate = datetime(2022,1,18)
            daysaway = 5
            self.assertEqual(get_date_in_x_market_days_away(daysaway,startdate),enddate)
            logger.info("Return date 5 days away over the weekend test successful")
        finally:
            pass

    def test_days_away_over_weekend(self):
        try:
            startdate = datetime(2022,8,7)
            enddate = datetime(2022,8,12)
            daysaway = 2
            self.assertEqual(get_date_in_x_market_days_away(daysaway,startdate),enddate)
            logger.info("Return date 2 days away over holiday test successful")
        finally:
            pass