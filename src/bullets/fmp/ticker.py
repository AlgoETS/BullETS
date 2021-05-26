

class Ticker:
    __slots__ = ["open", "low", "high", "close", "volume", "price"]

    def __init__(self, open=None, low=None, high=None,
                 close=None, volume=None, price=None):
        """
        Initializes the required variable for the Ticker
        """
        self.open = open
        self.low = low
        self.high = high
        self.close = close
        self.volume = volume
        self.price = price

    @classmethod
    def set_data(cls, data: dict):
        """
        Sets the data of the ticker corresponding with the desired date and time

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        open = round(data["open"], 2)
        low = round(data["low"], 2)
        high = round(data["high"], 2)
        close = round(data["close"], 2)
        volume = round(data["volume"], 2)
        price = round((open + close)/2, 2)

        return cls(open, low, high, close, volume, price)


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
        self.tickers = {}
        self.income_statement = {}
        self.balance_sheet = {}
        self.cash_flow = {}

        self.mktCap = None
        self.currency = ""
        self.exchange = ""
        self.sector = ""

    def get_ticker(self, date: str) -> Ticker:
        """
        Initializes the required variable for the Stock

        Args:
            date (str): instance of time to retrieve a ticker
        """
        if date not in self.tickers:
            return None
        else:
            return self.tickers[date]

    def get_income_statement(self, year: int, period: str):

        key = str(year) + " " + period

        if key not in self.income_statement:
            return None
        else:
            return self.income_statement[key]
