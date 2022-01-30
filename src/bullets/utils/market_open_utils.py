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

def get_date_in_x_market_days_away(lapse: int) -> date:
    """
    Gets the date that is x amount of market day(s) away
    Args:
        lapse: Number of days wanted
    Returns: The date that is the amount of market days away in date format
    """
    countdown = lapse
    today = datetime.today()
    while countdown > 0:
        today = today + timedelta(days=+1)
        if (is_market_open(today)): 
            countdown -= 1
    return today
