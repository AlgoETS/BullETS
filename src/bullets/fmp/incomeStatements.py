from bullets.fmp.apiCall import *
from bullets.fmp.ticker import *
from bullets.fmp.statements import *


class IncomeStatements(ApiCall):
    def __init__(self, client: Client):
        super().__init__(client)
        self.api_type = ApiType.IncomeStatement

    def load_data(self, stock: Stock, timespan="yearly"):
        """
        Retrieves the data from FMP

        Args:
            stock (Ticker): Ticker representing the desired stock
            timespan (str): the length of time the statement covers (either yearly or quarterly)
        """
        result = self.get_data(stock.symbol, timespan=timespan)

        for entry in result:
            date = entry["date"]
            period = entry["period"]
            key = date[0:4] + " " + period
            statement = IncomeStatement(entry)
            stock.income_statement[key] = statement
