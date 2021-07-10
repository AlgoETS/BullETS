from abc import abstractmethod

from bullets.portfolio.portfolio import Portfolio
from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from datetime import datetime

__all__ = ["Strategy"]


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
        self.start_time = start_time
        self.end_time = end_time
        self.starting_balance = starting_balance
        self.data_source = data_source
        self.portfolio = Portfolio(starting_balance, self.data_source)
        self.timestamp = None
        self.validate_start_data()

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

    def validate_start_data(self):
        if not isinstance(self.start_time, datetime) or not isinstance(self.end_time, datetime):
            raise TypeError("Invalid strategy date type")
        elif self.start_time > self.end_time or self.start_time == self.end_time:
            raise ValueError("Strategy start time has to be before end time")

        if not isinstance(self.resolution, Resolution):
            raise TypeError("Invalid strategy resolution type")

        if not isinstance(self.data_source, DataSourceInterface):
            raise TypeError("Invalid strategy data source type")

        if self.starting_balance is None or self.starting_balance <= 0:
            raise ValueError("Strategy starting balance should be positive")
