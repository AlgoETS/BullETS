

class PricePoint:
    def __init__(self, entry: dict):
        self.date = entry["date"]
        self.open = entry["open"]
        self.low = entry["low"]
        self.high = entry["high"]
        self.close = entry["close"]
        self.volume = entry["volume"]


class Stock:
    def __init__(self, symbol: str, resolution: str):
        """
        Initializes the required variable for the Stock
        Args:
            symbol (str): Unique identifier of a stock
            resolution (str): time jumps between ticker data
        """
        self.symbol = symbol
        self.resolution = resolution
        self.price_points = {}
        self.income_statement = {}
        self.balance_sheet = {}
        self.cash_flow = {}

        self.mktCap = None
        self.currency = ""
        self.exchange = ""
        self.sector = ""
