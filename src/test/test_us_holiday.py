import unittest
from datetime import datetime

from bullets.utils.holiday_date_util import us_holiday_list


class TestUsHoliday(unittest.TestCase):
    """
    source for dates: https://www.nyse.com/markets/hours-calendars
    """

    def test_martin_luther_king_day(self):
        date = datetime(2023, 1, 16)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_washingtons_birthday(self):
        date = datetime(2023, 2, 20)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_memorial_day(self):
        date = datetime(2023, 5, 29)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_juneteenth_national_independence_day(self):
        date = datetime(2023, 6, 19)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_independence_day(self):
        date = datetime(2023, 7, 4)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_labor_day(self):
        date = datetime(2023, 9, 4)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_thanksgiving_day(self):
        date = datetime(2023, 11, 23)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_christmas_day(self):
        date = datetime(2023, 12, 25)
        self.assertEqual(True, date in us_holiday_list(date.year))

    def test_good_friday(self):
        date = datetime(2023, 4, 7)
        self.assertEqual(True, date in us_holiday_list(date.year))

if __name__ == '__main__':
    unittest.main()
