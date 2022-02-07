import unittest
from datetime import datetime

from bullets import logger
from bullets.utils.holiday_date_util import us_holiday_list


class TestUsHoliday(unittest.TestCase):
    """
    source for dates: https://www.nyse.com/markets/hours-calendars
    """

    def test_martin_luther_king_day(self):
        try:
            date = datetime(2023, 1, 16)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Martin Luther King day test successful")
        finally:
            pass

    def test_washingtons_birthday(self):
        try:
            date = datetime(2023, 2, 20)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Washingtons birthday test successful")
        finally:
            pass

    def test_good_friday(self):
        try:
            date = datetime(2023, 4, 7)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Good friday test successful")
        finally:
            pass

    def test_memorial_day(self):
        try:
            date = datetime(2023, 5, 29)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Memorial day test successful")
        finally:
            pass

    def test_juneteenth_national_independence_day(self):
        try:
            date = datetime(2023, 6, 19)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Juneteenth national independence day test successful")
        finally:
            pass

    def test_independence_day(self):
        try:
            date = datetime(2023, 7, 4)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Independence day test successful")
        finally:
            pass

    def test_labor_day(self):
        try:
            date = datetime(2023, 9, 4)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Labor day test successful")
        finally:
            pass

    def test_thanksgiving_day(self):
        try:
            date = datetime(2023, 11, 23)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Thanksgiving day test successful")
        finally:
            pass

    def test_christmas_day(self):
        try:
            date = datetime(2023, 12, 25)
            self.assertEqual(True, date in us_holiday_list(date.year))
            logger.info("Christmas day test successful")
        finally:
            pass


if __name__ == '__main__':
    unittest.main()
