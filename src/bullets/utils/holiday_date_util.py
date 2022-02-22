from datetime import datetime, timedelta
from enum import IntEnum

Weekday = IntEnum('Weekday', 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday', start=0)
NthWeek = IntEnum('NthWeek', 'First Second Third Fourth Last', start=1)


def nth_day_of_nth_week(date: datetime, nth_week: int, week_day: int) -> datetime:
    temp_date = date.replace(day=1)
    adj = (week_day - temp_date.weekday()) % 7
    temp_date += timedelta(days=adj)
    temp_date += timedelta(weeks=nth_week - 1)
    return temp_date


def calc_good_friday(year: int) -> datetime:
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return datetime(year, month, day) + timedelta(days=-2)


def us_holiday_list(_year: int) -> []:
    holidays = []

    # New Year’s Day, January 1.
    holidays.append(datetime(year=_year, month=1, day=1))

    # Birthday of Martin Luther King, Jr., the third Monday in January.
    holidays.append(nth_day_of_nth_week(datetime(year=_year, month=1, day=1), NthWeek.Third, Weekday.Monday))

    # Washington’s Birthday, the third Monday in February.
    holidays.append(nth_day_of_nth_week(datetime(year=_year, month=2, day=1), NthWeek.Third, Weekday.Monday))

    # Good Friday, the Friday before Easter
    holidays.append(calc_good_friday(year=_year))

    # Memorial Day, the last Monday in May.
    holidays.append(nth_day_of_nth_week(datetime(year=_year, month=5, day=1), NthWeek.Last, Weekday.Monday))

    # Juneteenth National Independence Day, June 19.
    holidays.append(datetime(year=_year, month=6, day=19))

    # Independence Day, July 4.
    holidays.append(datetime(year=_year, month=7, day=4))

    # Labor Day, the first Monday in September.
    holidays.append(nth_day_of_nth_week(datetime(year=_year, month=9, day=1), NthWeek.First, Weekday.Monday))

    # Thanksgiving Day, the fourth Thursday in November.
    holidays.append(nth_day_of_nth_week(datetime(year=_year, month=11, day=1), NthWeek.Fourth, Weekday.Thursday))

    # Christmas Day, December 25.
    holidays.append(datetime(year=_year, month=12, day=25))

    # Adjust Saturday holidays to Friday and Sunday holidays to Monday
    for holiday in holidays:
        if holiday.weekday() == Weekday.Saturday:
            holiday += timedelta(days=-1)
        if holiday.weekday() == Weekday.Sunday:
            holiday += timedelta(days=1)

    return holidays
