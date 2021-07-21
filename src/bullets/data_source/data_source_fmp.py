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

    def store_price_points(self, symbol: str, start_date: datetime.date, end_date: datetime.date = None, limit: int = 1000):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
        else:
            stock = Stock(symbol, self.resolution)

        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value[0]) + "/"

        if end_date == None:
            nb_entree = limit
            if self.resolution == Resolution.HOURLY:
                nb_entree = math.ceil(nb_entree/6)
            elif self.resolution == Resolution.MINUTE:
                nb_entree = math.ceil(nb_entree/390)

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

            current_end_date = first_date
            if first_date <= start_date:
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
        self.store_price_points(symbol, date.date())
        
    def get_remaining_calls(self) -> int:
        body = {'data': {'key': self.token}}
        response = self.request(url="https://europe-west1-fmpdev-1d3ca.cloudfunctions.net/getRemainingCalls",
                                method="POST", body=body)

        return int(json.loads(response)['result'])

    def __get_interval__(self, start_time, end_time, resolution):
        return "from=" + str(start_time.date()) + "&to=" + str(end_time.date())

        return self.stocks[symbol].price_points[date].close