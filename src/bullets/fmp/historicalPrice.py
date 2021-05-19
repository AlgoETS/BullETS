from bullets.client import *
from bullets.fmp.ticker import *
from bullets.resolution import Resolution
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

    def get_data(self, symbol: str, resolution: str, start_date = "", end_date = "") -> str:
        """
        Retrieves the data from FMP

        Args:
            symbol (str): Unique identifier of a stock
            resolution (str): time jumps between ticker data
            start_date (str): the date to start collecting data
            end_date (str): the date to end collecting data

        Return:
            list of dictionary for each data point
        """
        modifier = ""
        if start_date != "":
            modifier += "from=" + start_date + "&"
        if end_date != "":
            modifier += "to=" + end_date + "&"
        if resolution == Resolution.daily:
            result = asyncio.run(self.client.request(f'/api/v3/historical-price-full/{symbol}', modifier))
        else:
            result = asyncio.run(self.client.request(f'/api/v3/historical-chart/{resolution}/{symbol}', modifier))
        return json.loads(result)

    def load_data(self, stock: Stock):
        """
        Retrieves the data from FMP

        Args:
            stock (Ticker): Ticker representing the desired stock
        """
        result = self.get_data(stock.symbol, stock.resolution)
        for entry in result:
            ticker = Ticker()
            date = entry["date"]
            entry.pop("date")
            ticker.set_data(entry)
            stock.ticker[date] = ticker
