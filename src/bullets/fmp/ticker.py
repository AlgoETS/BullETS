

class Ticker:
    def __init__(self):
        """
        Initializes the required variable for the Ticker
        """
        self.open = None
        self.low = None
        self.high = None
        self.close = None
        self.volume = None
        self.price = None

    def set_data(self, data: dict):
        """
        Sets the data of the ticker corresponding with the desired date and time

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        self.open = data["open"]
        self.low = data["low"]
        self.high = data["high"]
        self.close = data["close"]
        self.volume = data["volume"]
        self.price = round((self.open + self.close)/2, 2)


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

    def ticker(self, date: str):
        """
        Initializes the required variable for the Stock

        Args:
            date (str): instance of time to retrieve a ticker
        """
        if date not in self.tickers:
            ticker = Ticker()
            return ticker
        else:
            return self.tickers[date]
