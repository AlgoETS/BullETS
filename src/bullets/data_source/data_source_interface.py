from datetime import datetime

__all__ = ["Resolution", "DataSourceInterface"]

from enum import Enum


class Resolution(Enum):
    DAILY = "1day",
    HOURLY = "1hour",
    MINUTE = "1min"


class DataSourceInterface:
    def __init__(self):
        self.timestamp = None

    def get_price(self, symbol: str):
        pass
