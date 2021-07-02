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

        data = self.data_source.get_daily_historical_price()

        for element in data:
            self.strategy.data = element
            self.strategy.on_resolution()
            print(f"{element.price}$ / {element.ticker}")

        print("Strategy executed.")

    def attach(self, strategy: bullets.strategy.Strategy):
        self.strategy = strategy

    def buy(self, ticker: str, amount: float):
        # TODO: Implement runner buy logic
        print("We bought some stuff")

    def sell(self, ticker: str, amount: float):
        # TODO: Implement runner sell logic
        print("We sold some stuff")
