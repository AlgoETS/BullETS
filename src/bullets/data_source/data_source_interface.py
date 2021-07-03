from datetime import datetime


class BaseData:
    def __init__(self):
        self.timestamp = None

    def get_price(self):
        pass


class Tick:
    def __init__(self, symbol: str, date_time: datetime, price: float):
        self.symbol = symbol
        self.date_time = date_time
        self.price = price
