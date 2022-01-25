from datetime import datetime, timedelta, date
from bullets.data_source.data_source_interface import Resolution
from bullets.utils.holiday_date_util import us_holiday_list

def is_market_open(date: datetime, resolution: Resolution=Resolution.DAILY) -> bool:
        if date.weekday() >= 5:
            return False

        if resolution != Resolution.DAILY:
            if date.hour < 9 or date.hour > 16:
                return False
            elif date.hour == 16 and date.minute > 0:
                return False
            elif date.hour == 9 and date.minute < 30:
                return False

        return date not in us_holiday_list(date.year)

def get_date_x_days_away(x):
    countdown = x
    today = datetime.today()
    while countdown > 0:
        today = today + timedelta(days=+1)
        if (is_market_open(today)): 
            countdown -= 1
    return today
