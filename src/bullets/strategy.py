from abc import abstractmethod
from enum import Enum
from datetime import datetime
from bullets.portfolio.portfolio import Portfolio
from bullets.data_source.data_source_interface import DataSourceInterface

__all__ = ["Resolution", "Strategy"]


class Resolution(Enum):
    DAILY = 1,
    HOURLY = 2,
    MINUTE = 3,


class Strategy:

    """
    Base class for trading strategies. Extend this class and override the setup and on_resolution functions to make
    your own strategy.
    """
    def __init__(self,
                 resolution: Resolution,
                 start_time: datetime,
                 end_time: datetime,
                 starting_balance: float,
                 data_source: DataSourceInterface):
        self.resolution = resolution
        self.start_time = start_time  # TODO: Implement validation on strategy start_time
        self.end_time = end_time  # TODO: Implement validation on strategy end_time
        self.starting_balance = starting_balance
        self.data_source = data_source
        self.portfolio = Portfolio(starting_balance, self.data_source)
        self.timestamp = None

    """
        Extend this method to perform an operation that will be run on every resolution.
    """
    @abstractmethod
    def on_resolution(self):
        pass

    def update_time(self, timestamp):
        self.timestamp = timestamp
        self.data_source.timestamp = timestamp
        self.portfolio.timestamp = timestamp
