import ssl
from datetime import datetime
from abc import abstractmethod
import aiohttp
import asyncio
from enum import Enum


class Resolution(Enum):
    DAILY = "1day"
    HOURLY = "1hour"
    MINUTE = "1min"


class DataSourceInterface:
    def __init__(self):
        self.resolution = None
        self.timestamp = None

    @abstractmethod
    def get_price(self, symbol: str, timestamp: datetime = None, value: str = None):
        """
        Extend this method to get the price of a stock at a certain timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want.
            value: Value of the stock you want (open, close, low, high, etc)
        """
        pass

    @abstractmethod
    def get_historical_daily_prices(self, symbol: str, start_date: datetime.date, end_date: datetime.date = None):
        """
          Gets the historical prices of the given stock for the given interval period
          Args:
              symbol: Symbol of the stock/forex
              start_date: Starting time of the interval of historical prices
              end_date: Ending time of the interval of historical price. Default value is the time of the backtest
          Returns: An array of the closing price of the stock for every day between the interval
        """
    @staticmethod
    def request(url: str, method: str = "GET", body=None) -> str:
        """
        Performs a request on the requested endpoint at the base url.
        Args:
            url: address with endpoint to retrieve data
            method: method type to use to send request
            body: json data to send in the body
        Returns: JSON string with the response content
        """

        async def fetch() -> str:
            if url:
                async with aiohttp.ClientSession() as session:
                    async with session.request(url=url, method=method, ssl=ssl.SSLContext(), json=body) as response:
                        if response.status == 200:
                            return await response.text()

        return asyncio.get_event_loop().run_until_complete(fetch())
