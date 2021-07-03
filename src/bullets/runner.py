from bullets.strategy import Strategy, Resolution
import datetime

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
        return [datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 2)]
        # TODO Get time of each tick in the backtest interval given the resolution
