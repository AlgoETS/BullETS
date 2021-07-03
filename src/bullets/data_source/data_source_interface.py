from datetime import datetime


class DataSourceInterface:
    def __init__(self):
        self.timestamp = None

    def get_price(self, symbol: str):
        pass


class Tick:
    def __init__(self, symbol: str, date_time: datetime, price: float):
        self.symbol = symbol
        self.date_time = date_time
        self.price = price
