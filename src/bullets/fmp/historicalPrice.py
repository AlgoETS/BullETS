from bullets.client import *
from bullets.ticker import Ticker
import json
import asyncio


class HistoricalPrice:
    def __init__(self, client: Client):
        """
        Initializes the required variable for the Historical price

        Args:
            client (Client): the client who wants to make a query
        """
        self.client = client

    def get_data(self, symbol: str, resolution: str) -> str:
        """
        Retrieves the data from FMP

        Args:
            symbol (str): Unique identifier of a stock
            resolution (str): time jumps between ticker data

        Return:
            list of dictionary for each data point
        """
        result = asyncio.run(self.client.request(f'/api/v3/historical-chart/{resolution}/{symbol}'))
        return json.loads(result)

    def load_data(self, ticker: Ticker):
        """
        Retrieves the data from FMP

        Args:
            ticker (Ticker): Ticker representing the desired stock
        """
        data = {}
        result = self.get_data(ticker.symbol, ticker.resolution)
        for entry in result:
            date = entry["date"]
            entry.pop("date")
            data[date] = entry
        ticker.data = data
