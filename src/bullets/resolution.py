from enum import Enum


class Resolution(Enum):
    min = "1min"
    min5 = "5min"
    min15 = "15min"
    min30 = "30min"
    hour = "1hour"
    hour4 = "4hour"
    daily = "1day"
