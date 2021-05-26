from bullets.client import *
from bullets.fmp.apiType import *
from bullets.resolution import Resolution
import datetime as dt
import asyncio
import json


class ApiCall:
    baseURL = 'https://financialmodelingprep.com'

    def __init__(self, client: Client):
        """
        Initializes the required variable for the ApiCall

        Args:
            client (Client): the client who wants to make a query
        """
        self.client = client
        self.api_type = None

    def create_request(self, endpoint: str, modifier: str):
        return f"{self.baseURL}{endpoint}?{modifier}apikey={self.client.token}"

    @staticmethod
    def set_modifier(timespan="yearly", start_date="", end_date="", limit=0):
        modifier = ""
        if start_date != "":
            modifier += "from=" + start_date + "&"
        if end_date != "":
            modifier += "to=" + end_date + "&"
        if timespan == "quarterly":
            modifier += "period=quarter&"
        if limit != 0:
            modifier += "limit=" + str(limit) + "&"
        return modifier

    def set_endpoint(self, symbol: str, resolution: str):

        if resolution == Resolution.Daily and self.api_type == ApiType.HistoricalPrice:
            api = "historical-price-full"
            res = ""
        elif self.api_type != ApiType.HistoricalPrice:
            api = self.api_type
            res = ""
        else:
            api = self.api_type
            res = resolution + "/"

        return f"/api/v3/{api}/{res}{symbol}"

    def get_data(self, symbol: str, resolution="",
                 timespan="yearly", start_date="", end_date="", limit=0):
        """
        Retrieves the data from FMP

        Args:
            symbol (str): Unique identifier of a stock
            resolution (str): time jumps between ticker data
            timespan (str): Use to differentiate between quarterly and yearly statements
            start_date (str): the date to start collecting data
            end_date (str): the date to end collecting data
            limit (int): The max amount of data point to pull

        Return:
            list of dictionary for each data point
        """
        endpoint = self.set_endpoint(symbol, resolution)
        modifier = self.set_modifier(timespan, start_date, end_date, limit)
        url = self.create_request(endpoint, modifier)
        result = asyncio.run(self.client.request(url))
        return json.loads(result)

    @staticmethod
    def is_all_data_retrieved(expected_start_date: str, received_start_date: str):
        start_date = dt.date(int(expected_start_date[0:4]), int(expected_start_date[5:7]), int(expected_start_date[8:10]))
        compare_date = dt.date(int(received_start_date[0:4]), int(received_start_date[5:7]), int(received_start_date[8:10]))

        start_date += dt.timedelta(days=1)

        if start_date.weekday() >= 5:
            while start_date.weekday() != 0:
                start_date += dt.timedelta(days=1)

        if start_date < compare_date:
            return False
        else:
            return True


