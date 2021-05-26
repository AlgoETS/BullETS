from bullets.fmp.apiCall import *
from bullets.fmp.ticker import *


class CompanyProfile(ApiCall):
    def __init__(self, client: Client):
        super().__init__(client)
        self.api_type = ApiType.Profile

    def load_data(self, stock: Stock):
        """
        Retrieves the data from FMP

        Args:
            stock (Ticker): Ticker representing the desired stock
        """
        result = self.get_data(stock.symbol)[0]

        stock.mktCap = result["mktCap"]
        stock.currency = result["currency"]
        stock.exchange = result["exchangeShortName"]
        stock.sector = result["sector"]
