import datetime
import json
import math

from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets.data_source.recorded_data import *


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution):
        super().__init__()
        self.token = token
        self.resolution = resolution
        self.stocks = {}

    def __store_price_points__(self, symbol: str, start_date: datetime.date, end_date: datetime.date = None,
                               limit: int = 1000):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
        else:
            stock = Stock(symbol, self.resolution)

        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value[0]) + "/"

        if end_date is None:
            nb_entree = limit
            if self.resolution == Resolution.HOURLY:
                nb_entree = math.ceil(nb_entree / 6)
            elif self.resolution == Resolution.MINUTE:
                nb_entree = math.ceil(nb_entree / 390)

            end_date = start_date + datetime.timedelta(days=nb_entree)
            if end_date > datetime.date.today():
                end_date = datetime.date.today()

        current_end_date = end_date
        finished = False

        while not finished:
            interval = "from=" + str(start_date) + "&to=" + str(current_end_date)
            url = self.URL_BASE_FMP + url_resolution + symbol + "?" + interval + "&apikey=" + self.token
            response = self.request(url)

            if response == "{ }":
                break
            result = json.loads(response)
            if self.resolution == Resolution.DAILY:
                data = result["historical"]
            else:
                data = result

            first_date = current_end_date

            for entry in data:
                price_point = PricePoint(entry)
                if self.resolution == Resolution.DAILY:
                    stock_date = datetime.datetime.strptime(price_point.date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                else:
                    stock_date = datetime.datetime.strptime(price_point.date, "%Y-%m-%d %H:%M:%S")

                stock.price_points[stock_date] = price_point
                first_date = stock_date.date()
            if current_end_date == first_date:
                finished = True
            else:
                current_end_date = first_date

            if first_date <= start_date:
                finished = True

        self.stocks[symbol] = stock

    def get_price(self, symbol: str, timestamp: datetime = None) -> int:
        """
        Gets the information of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want. If you want to the current time of the backtest, leave empty
        Returns: The stock information at the given timestamp
        """
        if timestamp is None:
            date = self.timestamp
        else:
            date = timestamp

        value = self.__get_cached_price__(symbol, date)

        if value is None:
            self.__store_price_points__(symbol, date.date())
            new_value = self.__get_cached_price__(symbol, date)
            if new_value is None:
                return None
            else:
                return new_value
        else:
            return value

    def __get_cached_price__(self, symbol: str, date: datetime):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
            if date in stock.price_points:
                return stock.price_points[date].close

    def get_remaining_calls(self) -> int:
        body = {'data': {'key': self.token}}
        response = self.request(url="https://europe-west1-fmpdev-1d3ca.cloudfunctions.net/getRemainingCalls",
                                method="POST", body=body)

        return int(json.loads(response)['result'])
