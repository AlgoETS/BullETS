from bullets.strategy import Strategy
from bullets.data_source.data_source_interface import BaseData
from bullets.portfolio.portfolio import Portfolio

__all__ = ["Runner"]


class Runner:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def start(self):
        if self.strategy is None:
            raise TypeError("No strategy was attached to the runner.")

        moments = [] # TODO Get time of each tick in the backtest interval given the resolution

        for moment in moments:
            self.strategy.update_time(moment)
            self.strategy.on_resolution()
