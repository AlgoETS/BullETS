import datetime
import json
import asyncio
import aiohttp

from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from urllib.request import urlopen
from types import SimpleNamespace


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution, symbol: str, start_time: datetime, end_time: datetime):
        super().__init__()
        self.token = token
        self.resolution = resolution
        self.symbol = symbol
        self.start_time = start_time
        self.end_time = end_time
        self.data = {}

        self.build_data_source()

    def build_data_source(self):
        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value[0]) + "/"
        current_end_date = self.end_time
        finished = False
        while not finished:
            interval = "from=" + str(self.start_time.date()) + "&to=" + str(current_end_date.date())
            url = self.URL_BASE_FMP + url_resolution + self.symbol + "?" + interval + "&apikey=" + self.token
            response = self.request(url)
            if response == "{ }":
                return None
            result = json.loads(response)
            if self.resolution == Resolution.DAILY:
                data = result["historical"]
            else:
                data = result
            first_date = current_end_date
            for entry in data:
                stock = Stock(entry)
                if self.resolution == Resolution.DAILY:
                    stock_date = datetime.datetime(int(stock.date[0:4]), int(stock.date[5:7]), int(stock.date[8:10]))
                else:
                    stock_date = datetime.datetime(int(stock.date[0:4]), int(stock.date[5:7]), int(stock.date[8:10]),
                                                   int(stock.date[11:13]), int(stock.date[14:16]),
                                                   int(stock.date[17:19]))

                self.data[stock_date] = stock
                first_date = stock_date
            current_end_date = first_date
            if first_date <= self.start_time:
                finished = True

    def get_price(self, timestamp: datetime = None):
        """
        Gets the information of the stock at the current timestamp
        Args:
            timestamp: Time of the data you want. If you want to the current time of the backtest, leave empty
        Returns: The stock information at the given timestamp
        """
        if timestamp is None:
            date = self.timestamp
        else:
            date = datetime

        for increment in self.data:
            stock = self.data[increment]
            if increment == date:
                return stock.close
        return None


class Stock:
    def __init__(self, json_stock: dict):
        self.date = json_stock["date"]
        self.open = json_stock["open"]
        self.low = json_stock["low"]
        self.high = json_stock["high"]
        self.close = json_stock["close"]
        self.volume = json_stock["volume"]
