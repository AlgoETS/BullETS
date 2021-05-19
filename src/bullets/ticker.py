

class Ticker:
    def __init__(self, symbol: str, resolution: str):
        """
        Initializes the required variable for the Ticker

        Args:
            symbol (str): Unique identifier of a stock
            resolution (str): time jumps between ticker data
        """
        self.symbol = symbol
        self.resolution = resolution
        self.date = ""
        self.open = None
        self.low = None
        self.high = None
        self.close = None
        self.volume = None
        self.price = None
        self.data = {}

    def set_date(self, date: str, time: str):
        """
        Sets the data of the ticker corresponding with the desired date and time

        Args:
            date (str): the date of the desired ticker in the format yyyy-mm-dd
            date (str): the time of the desired ticker in the format hh:mm:ss

        Note:
            Datetime functions can be used as arguments (in str format)
        """
        self.date = date + " " + time

        self.open = self.data[self.date]["open"]
        self.low = self.data[self.date]["low"]
        self.high = self.data[self.date]["high"]
        self.close = self.data[self.date]["close"]
        self.volume = self.data[self.date]["volume"]
        self.price = (self.open + self.close)/2


