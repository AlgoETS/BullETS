from bullets.strategy import Strategy, Resolution
from datetime import datetime, timedelta

__all__ = ["Runner"]


class Runner:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def start(self):
        """
        Starts the backtest
        """
        if self.strategy is None:
            raise TypeError("No strategy was attached to the runner.")

        moments = self.get_moments(self.strategy.resolution, self.strategy.start_time, self.strategy.end_time)

        for moment in moments:
            self.strategy.update_time(moment)
            self.strategy.on_resolution()

        print("Backtest complete")

    def get_moments(self, resolution: Resolution, start_time: datetime, end_time: datetime):
        """
        Gets the all the moments of the backtest
        Args:
            resolution: Resolution of the backtest
            start_time: DateTime at which the backtest starts
            end_time: DateTime at which the backtest end
        Returns: List of tradeable datetimes given the interval and resolutions
        """
        moments = []
        current_time = start_time

        while current_time != end_time:
            if resolution == Resolution.DAILY:
                current_time = current_time + timedelta(days=1)
            elif resolution == Resolution.HOURLY:
                current_time = current_time + timedelta(hours=1)
            elif resolution == Resolution.MINUTE:
                current_time = current_time + timedelta(minutes=1)

            if self.is_market_open(current_time):
                moments.append(current_time)

        return moments

    def is_market_open(self, time: datetime) -> bool:
        """
        Determines if the market is open at the specified time.
        Args:
            time: Datetime to verify

        Returns: True if the market is open, False if the market is closed

        """

        # TODO: Determine if the date provided is a holiday

        if time.weekday() <= 5:
            return False
        elif time.hour < 9 or time.hour > 16:
            return False
        elif time.hour == 9 and time.minute < 30:
            return False
        elif time.hour == 16 and time.minute > 0:
            return False

        return True
