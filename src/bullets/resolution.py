from enum import Enum


class Resolution(str, Enum):
    Minute = "1min"
    Min5 = "5min"
    Min15 = "15min"
    Min30 = "30min"
    Hour = "1hour"
    Hour4 = "4hour"
    Daily = "1day"

    def __str__(self):
        return self.value


class Timespan(str, Enum):
    Quarterly = "quarterly"
    Yearly = "yearly"

    def __str__(self):
        return self.value
