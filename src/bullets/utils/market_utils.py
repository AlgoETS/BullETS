from datetime import datetime, timedelta, date
from bullets.data_source.data_source_interface import Resolution
from bullets.utils.holiday_date_util import us_holiday_list


def is_market_open(date: datetime, resolution: Resolution = Resolution.DAILY) -> bool:
    """
    Returns if the market is open on a given day
    Args:
        date: Checks if the market is open on the date given
        resolution: Will check if market is open at a specific time if the resolution demands it
    Returns: True if the market is open, else False
    """
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


def get_date_in_x_market_days_away(lapse: int, start_date: datetime = datetime.today()) -> date:
    """
    Gets the date that is x amount of market day(s) away
    Args:
        lapse: Number of days wanted
        start_date: date at which the function starts, default: present day
    Returns: The date that is the amount of market days away in date format
    """
    countdown = lapse
    today = start_date
    while countdown > 0:
        today = today + timedelta(days=+1)
        if is_market_open(today):
            countdown -= 1
    return today


def get_moments(resolution: Resolution, start_time: datetime, end_time: datetime):
    moments = []
    current_time = start_time

    while current_time != end_time:
        if resolution == Resolution.DAILY:
            current_time = current_time + timedelta(days=1)
        elif resolution == Resolution.HOURLY:
            current_time = current_time + timedelta(hours=1)
        elif resolution == Resolution.MINUTE:
            current_time = current_time + timedelta(minutes=1)

        if is_market_open(current_time, resolution):
            moments.append(current_time)

    return moments
