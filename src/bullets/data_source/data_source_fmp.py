import datetime
import json

from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from urllib.request import urlopen
from types import SimpleNamespace


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution):
        super().__init__()
        self.token = token
        self.resolution = resolution

    def get_price(self, symbol: str):
        """
        Gets the information of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
        Returns: The stock information at the given timestamp
        """

        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value[0]) + "/"

        interval = self.get_interval(self.timestamp, self.timestamp, self.resolution)

        url = self.URL_BASE_FMP + url_resolution + symbol + "?" + interval + "&apikey=" + self.token

        response = urlopen(url)
        data = response.read().decode("utf-8")
        result = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        if self.resolution == Resolution.DAILY:
            stock = result.historical[0]
        else:
            stock = self.find_element_by_date(result)

        return Stock(json_stock=stock).close

    def get_interval(self, start_time, end_time, resolution):
        return "from=" + str(start_time.date()) + "&to=" + str(end_time.date())

    def find_element_by_date(self, intervals):
        for interval in intervals:
            date = datetime.datetime.fromisoformat(interval.date)
            if date == self.timestamp:
                return interval


class Stock:
    def __init__(self, json_stock: dict):
        self.date = json_stock.date
        self.open = json_stock.open
        self.low = json_stock.low
        self.high = json_stock.high
        self.close = json_stock.close
        self.volume = json_stock.volume


if __name__ == '__main__':
    source = FmpDataSource("878bd792d690ec6591d21a52de0b6774", Resolution.MINUTE)
    source.timestamp = datetime.datetime(2019, 3, 12, 15, 57)
    stock = source.get_price("AAPL")
    print(stock.date)
    print(stock.open)
    print(stock.low)
    print(stock.high)
    print(stock.close)
    print(stock.volume)
