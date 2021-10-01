from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets.runner import Runner
from datetime import datetime, timedelta


class Indicators:
    def __init__(self, data_source: DataSourceInterface):
        self.data_source = data_source

    def sma(self, symbol: str, period: int, date: datetime = None):
        """
        Calculates the Simple Moving Average
        Args:
            symbol: Stock symbol
            period: number of days for the average
            date: Date of average / start date
        Returns:
            sma: Average stock price for the given range
        """

        if date is None:
            date = self.data_source.timestamp
        else:
            date = date

        values = []

        for x in range(period):
            #Make sure market is open
            while not Runner._is_market_open(date, Resolution.DAILY):
                date -= timedelta(days=1)

            ##Go back one day
            date -= timedelta(days=1)

        for x in range(period):
            # Make sure market is open
            while not Runner._is_market_open(date, Resolution.DAILY):
                date += timedelta(days=1)

            #Fetch stock value
            price = self.data_source.get_price(symbol=symbol, timestamp=date)
            if price is not None:
                values.append(price)

            ##Go forward one day
            date += timedelta(days=1)

        #Calculate SMA
        sma = sum(values) / len(values)

        return sma

    def ema(self, symbol: str, period: int, date: datetime = None, smoothing: int = 2):
        """
        Calculates the Simple Moving Average
        Args:
            symbol: Stock symbol
            period: number of days for the average
            date: Date of average / start date
            smoothing: weighted importance of latest data, higher number gives more weight to more recent data
        Returns:
            ema: Exponential average stock price for the given range
        """

        if date is None:
            date = self.data_source.timestamp
        else:
            date = date

        multiplier = smoothing/(period + 1)

        for x in range(period):
            #Make sure market is open
            while not Runner._is_market_open(date, Resolution.DAILY):
                date -= timedelta(days=1)

            ##Go back one day
            date -= timedelta(days=1)

        ema = self.sma(symbol, period, date)
        date += timedelta(days=1)

        for x in range(period):
            # Make sure market is open
            while not Runner._is_market_open(date, Resolution.DAILY):
                date += timedelta(days=1)

            price = self.data_source.get_price(symbol=symbol, timestamp=date)
            if price is not None:
                ema = price*multiplier + ema*(1-multiplier)

            ##Go forward one day
            date += timedelta(days=1)

        return ema

    def macd(self, symbol, date: datetime = None):
        """
        Calculates the Simple Moving Average
        Args:
            symbol: Stock symbol
            date: Calculated date / start date
        Returns:
            MACD
        """

        if date is None:
            date = self.data_source.timestamp
        else:
            date = date

        return self.ema(symbol, 12, date) - self.ema(symbol, 26, date)
