from datetime import datetime
import aiohttp
import asyncio

__all__ = ["Resolution", "DataSourceInterface"]

from enum import Enum


class Resolution(Enum):
    DAILY = "1day",
    HOURLY = "1hour",
    MINUTE = "1min"


class DataSourceInterface:
    def __init__(self):
        self.timestamp = None

    def get_price(self, symbol: str, timestamp:datetime = None):
        pass

    @staticmethod
    def request(url: str, method: str = "GET", body=None) -> str:
        """
        Performs a request on the requested endpoint at the base url.
        Args:
            url (str): address with endpoint to retrieve data
            method (str): method type to use to send request
            body: json data to send in the body

        Returns:
            JSON string with the response content
        """

        async def fetch() -> str:
            if url:
                async with aiohttp.ClientSession() as session:
                    async with session.request(url=url, method=method, json=body) as response:
                        if response.status == 200:
                            return await response.text()

        return asyncio.get_event_loop().run_until_complete(fetch())
