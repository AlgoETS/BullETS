from bullets.fmp.apiCall import *
from bullets.fmp.ticker import *
from bullets.resolution import Resolution


class HistoricalPrice(ApiCall):
    def __init__(self, client: Client):
        super().__init__(client)
        self.api_type = ApiType.HistoricalPrice

    def load_data(self, stock: Stock, start_date="", end_date=""):
        """
        Retrieves the data from FMP

        Args:
            stock (Ticker): Ticker representing the desired stock
            start_date (str): the date to start collecting data
            end_date (str): the date to end collecting data
        """
        date = ""
        finished = False
        while not finished:
            if stock.resolution == Resolution.Daily:
                result = self.get_data(stock.symbol, resolution=stock.resolution,
                                       start_date=start_date, end_date=end_date)["historical"]
            else:
                result = self.get_data(stock.symbol, resolution=stock.resolution,
                                       start_date=start_date, end_date=end_date)

            for entry in result:
                date = entry["date"]
                ticker = Ticker.set_data(entry)
                stock.tickers[date] = ticker
            print(start_date)
            print(date)
            finished = self.is_all_data_retrieved(start_date, date[0:10])
            end_date = date[0:10]
