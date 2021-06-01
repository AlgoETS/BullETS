from bullets.fmp.apiType import *
from bullets.resolution import *
from datetime import date, timedelta


class ApiCall:
    baseURL = 'https://financialmodelingprep.com'

    def __init__(self, token: str, api_type=""):
        """
        Initializes the required variable for the ApiCall

        Args:
            token (str): API key from FinancialModelPrep
            api_type (str): type of data requested
        """
        self.token = token
        self.type = api_type

    def create_request(self, endpoint: str, modifier: str) -> str:
        return f"{self.baseURL}{endpoint}?{modifier}apikey={self.token}"

    @staticmethod
    def set_modifier(timespan="yearly", start_date=date(1, 1, 1), end_date=date(1, 1, 1), limit=0) -> str:
        modifier = ""
        if start_date != date(1, 1, 1):
            modifier += "from=" + str(start_date) + "&"
        if end_date != date(1, 1, 1):
            modifier += "to=" + str(end_date) + "&"
        if timespan == "quarterly":
            modifier += "period=quarter&"
        if limit != 0:
            modifier += "limit=" + str(limit) + "&"
        return modifier

    def set_endpoint(self, symbol: str, resolution: str) -> str:

        if resolution == Resolution.Daily and self.type == ApiType.HistoricalPrice:
            api = "historical-price-full"
            res = ""
        elif self.type != ApiType.HistoricalPrice:
            api = self.type
            res = ""
        else:
            api = self.type
            res = resolution + "/"

        return f"/api/v3/{api}/{res}{symbol}"

    def get_data(self, symbol: str, resolution="", timespan=Timespan.Yearly,
                 start_date=date(1, 1, 1), end_date=date(1, 1, 1), limit=0) -> str:
        """
        Retrieves the data from FMP

        Args:
            symbol (str): Unique identifier of a stock
            resolution (str): time jumps between ticker data
            timespan (str): Use to differentiate between quarterly and yearly statements
            start_date (date): the date to start collecting data
            end_date (date): the date to end collecting data
            limit (int): The max amount of data point to pull

        Return:
            list of dictionary for each data point
        """
        endpoint = self.set_endpoint(symbol, resolution)
        modifier = self.set_modifier(timespan, start_date, end_date, limit)
        return self.create_request(endpoint, modifier)

    @staticmethod
    def is_all_data_retrieved(start_date: date, compare_date: date) -> bool:

        if start_date.weekday() >= 5:
            while start_date.weekday() != 0:
                start_date += timedelta(days=1)

        if start_date < compare_date:
            return False
        else:
            return True


