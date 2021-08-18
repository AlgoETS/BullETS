from abc import abstractmethod
from datetime import datetime
from bullets.portfolio.portfolio import Portfolio
from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets import logger


class Strategy:
    def __init__(self, resolution: Resolution, start_time: datetime, end_time: datetime, starting_balance: float,
                 data_source: DataSourceInterface, slippage_percent: int = 25, transaction_fees: int = 1):
        self.resolution = resolution
        self.start_time = start_time
        self.end_time = end_time
        self.starting_balance = starting_balance
        self.data_source = data_source
        self.slippage_percent = slippage_percent
        self.transaction_fees = transaction_fees
        self.timestamp = None
        self.portfolio = Portfolio(self.starting_balance, self.data_source, self.slippage_percent,
                                   self.transaction_fees)
        self._validate_start_data()

    @abstractmethod
    def on_resolution(self):
        """
            Extend this method to perform an operation that will be run on every resolution.
        """
        pass

    @abstractmethod
    def on_start(self):
        """
            Extend this method to perform an operation that will be run at the start of the strategy.
        """
        pass

    @abstractmethod
    def on_finish(self):
        """
            Extend this method to perform an operation that will be run at the end of the strategy.
        """
        pass

    def update_time(self, timestamp):
        """
        Updates all timestamps (strategy, datasource, portfolio) to a specific timestamp
        Args:
            timestamp: the new timestamp wanted
        """
        self.timestamp = timestamp
        self.data_source.timestamp = timestamp
        self.portfolio.timestamp = timestamp

    def _validate_start_data(self):
        if not isinstance(self.start_time, datetime) or not isinstance(self.end_time, datetime):
            raise TypeError("Invalid strategy date type")
        elif self.start_time > self.end_time or self.start_time == self.end_time:
            raise ValueError("Strategy start time has to be before end time")

        if not isinstance(self.resolution, Resolution):
            raise TypeError("Invalid strategy resolution type")
        elif self.resolution is not Resolution.DAILY:
            logger.warning("Resolution not set to daily, market orders will not consider slippage, split or dividend")

        if not isinstance(self.data_source, DataSourceInterface):
            raise TypeError("Invalid strategy data source type")

        if self.starting_balance is None or self.starting_balance <= 0:
            raise ValueError("Strategy starting balance should be positive")

        if self.slippage_percent is None or self.slippage_percent < 0 or self.slippage_percent > 100:
            raise ValueError("Slippage percent should be between 0 and 100")

        if self.transaction_fees is None or self.transaction_fees < 0:
            raise ValueError("Transaction fees should be positive or 0")
