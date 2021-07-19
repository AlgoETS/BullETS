import datetime
import json

from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from types import SimpleNamespace


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution):
        super().__init__()
        self.token = token
        self.resolution = resolution


    def get_price(self, symbol: str, timestamp:datetime = None):
        """
        Gets the information of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want. If you want to the current time of the backtest, leave empty
        Returns: The stock information at the given timestamp
        """
        timestamp = self.__get_timestamp__(timestamp)
        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value[0]) + "/"

        interval = self.__get_interval__(timestamp, timestamp, self.resolution)

        url = self.URL_BASE_FMP + url_resolution + symbol + "?" + interval + "&apikey=" + self.token

        response = self.request(url)

        if response == "{ }":
            return None

        result = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))

        if self.resolution == Resolution.DAILY:
            stock = result.historical[0]
        else:
            stock = self.__find_element_by_date__(result, timestamp)

        return Stock(json_stock=stock).close

    def get_remaining_calls(self) -> int:
        body = {'data': {'key': self.token}}
        response = self.request(url="https://europe-west1-fmpdev-1d3ca.cloudfunctions.net/getRemainingCalls",
                                method="POST", body=body)

        return int(json.loads(response)['result'])

    def __get_interval__(self, start_time, end_time, resolution):
        return "from=" + str(start_time.date()) + "&to=" + str(end_time.date())

    def __find_element_by_date__(self, intervals, timestamp):
        for interval in intervals:
            date = datetime.datetime.fromisoformat(interval.date)
            if date == timestamp:
                return interval

    def __get_timestamp__(self, timestamp: datetime = None):
        if timestamp is None:
            return self.timestamp
        else:
            return timestamp


class Stock:
    def __init__(self, json_stock: dict):
        self.date = json_stock.date
        self.open = json_stock.open
        self.low = json_stock.low
        self.high = json_stock.high
        self.close = json_stock.close
        self.volume = json_stock.volume
