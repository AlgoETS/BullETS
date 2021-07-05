import datetime
import json
from bullets.data_source.data_source_interface import DataSourceInterface
from urllib.request import urlopen
from types import SimpleNamespace


class FmpDataSource(DataSourceInterface):
    BASE_URL = 'https://financialmodelingprep.com'

    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def get_price(self, symbol: str):
        """
        Gets the information of the stock at the current timestamp in the backtest
        Args:
            symbol: Symbol of the stock
        Returns: The tick information of the stock at the given timestamp
        """
        url = "https://financialmodelingprep.com/api/v3/historical-price-full/AAPL" \
              "?from=" + str(self.timestamp.date()) + "&to=" + str(self.timestamp.date()) + \
              "&apikey=878bd792d690ec6591d21a52de0b6774"

        response = urlopen(url)
        data = response.read().decode("utf-8")
        result = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        return Stock(json_stock=result.historical[0])


class Stock:
    def __init__(self, json_stock: dict):
        self.date = json_stock.date
        self.open = json_stock.open
        self.low = json_stock.low
        self.high = json_stock.high
        self.close = json_stock.close
        self.volume = json_stock.volume


if __name__ == '__main__':

    source = FmpDataSource("878bd792d690ec6591d21a52de0b6774")
    source.timestamp = datetime.datetime(2019, 3, 12)
    print(source.get_price("AAPL").open)
