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

    def test_valid_weekday_daily_market_open(self):
        try:
            date = datetime(2022, 2, 1, 1, 30, 20)
            self.assertEqual(True, is_market_open(date, Resolution.DAILY))
            logger.info("Valid weekday daily market open test successful")
        finally:
            pass

    def test_valid_weekday_sub_daily_market_open(self):
        try:
            date = datetime(2022, 2, 2, 13, 30, 20)
            self.assertEqual(True, is_market_open(date, Resolution.MINUTE))
            logger.info("Valid weekday sub daily market open test successful")
        finally:
            pass

    def test_invalid_weekend_daily_market_open(self):
        try:
            date = datetime(2022, 2, 3, 1, 30, 20)
            self.assertEqual(True, is_market_open(date, Resolution.DAILY))
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
            start_date = datetime(2022, 2, 7)
            end_date = datetime(2022, 2, 11)
            days_away = 4
            self.assertEqual(True, get_date_in_x_market_days_away(days_away, start_date) == end_date)
            logger.info("Return date 4 days away same week test successful")
        finally:
            pass

    def test_days_away_over_weekend(self):
        try:
            start_date = datetime(2022, 2, 7)
            end_date = datetime(2022, 2, 14)
            days_away = 5
            self.assertEqual(True, get_date_in_x_market_days_away(days_away, start_date) == end_date)
            logger.info("Return date 5 days away over the weekend test successful")
        finally:
            pass

    def test_days_away_over_holiday(self):
        try:
            start_date = datetime(2022, 2, 18)
            end_date = datetime(2022, 2, 22)
            days_away = 1
            self.assertEqual(True, get_date_in_x_market_days_away(days_away, start_date) == end_date)
            logger.info("Return date 2 days away over holiday test successful")
        finally:
            pass


if __name__ == '__main__':
    unittest.main()
