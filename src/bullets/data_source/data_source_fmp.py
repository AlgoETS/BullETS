import datetime
import json
import asyncio
import aiohttp

from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets.data_source.recorded_data import *


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution):
        super().__init__()
        self.token = token
        self.resolution = resolution
        self.stocks = {}

    def store_price_points(self, symbol: str, timestamp: datetime, limit: int = 1000):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
        else:
            stock = Stock(symbol, self.resolution)

        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value[0]) + "/"
        finished = False
        nb_entries = limit

        while not finished:
            interval = "from=" + str(timestamp) + "&limit=" + str(nb_entries)
            url = self.URL_BASE_FMP + url_resolution + symbol + "?" + interval + "&apikey=" + self.token
            response = self.request(url)

            if response == "{ }":
                break
            result = json.loads(response)
            if self.resolution == Resolution.DAILY:
                data = result["historical"]
            else:
                data = result

            for entry in data:
                price_point = PricePoint(entry)
                if self.resolution == Resolution.DAILY:
                    stock_date = datetime.datetime.strptime(price_point.date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                else:
                    stock_date = datetime.datetime.strptime(price_point.date, "%Y-%m-%d %H:%M:%S")

                stock.price_points[stock_date] = price_point

            nb_entries -= len(data)

            if nb_entries <= 0:
                finished = True

        self.stocks[symbol] = stock

    def get_market_open_close(self):
        url = self.URL_BASE_FMP + "is-the-market-open?apikey=" + self.token
        response = self.request(url)
        result = json.loads(response)
        holidays = []
        for entry in result["stockMarketHolidays"]:
            del entry["year"]
            for date in entry.values():
                holidays.append(datetime.datetime.strptime(date, "%Y-%m-%d"))
        return holidays

    def get_price(self, symbol: str, timestamp: datetime = None) -> int:
        """
        Gets the information of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want. If you want to the current time of the backtest, leave empty
        Returns: The stock information at the given timestamp
        """
        if timestamp is None:
            date = datetime.datetime.now
        else:
            date = self.timestamp

        if symbol in self.stocks:
            stock = self.stocks[symbol]
            if date in stock.price_points:
                return stock.price_points[date].close

        self.store_price_points(symbol, datetime.date(date.year, date.month, date.day))

        return self.stocks[symbol].price_points[date].close

