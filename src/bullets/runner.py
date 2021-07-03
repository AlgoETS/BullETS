import bullets.strategy
from bullets.data.base import BaseData

__all__ = ["Runner"]


class Runner:
    def __init__(self, data_source: BaseData):
        self.data_source = data_source
        self.strategy = None

    def start(self):
        if self.strategy is None:
            raise TypeError("No strategy was attached to the runner.")

        # TODO Get time of each tick for the resolution and backtest interval
        data = self.data_source.get_daily_historical_price()

        for element in data:
            # TODO Update date time of the data source and portfolio
            self.strategy.data = element
            self.data_source.date = new_date
            self.strategy.on_resolution()
            print(f"{element.price}$ / {element.ticker}")

        print("Strategy executed.")

    def attach(self, strategy: bullets.strategy.Strategy):
        self.strategy = strategy

