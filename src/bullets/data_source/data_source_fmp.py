import json
from datetime import date, timedelta

from bullets.data_source.data_source_interface import DataSourceInterface
from bullets.data_source.recorded_data import *
from bullets.data_storage.cache_storage import *
from bullets.data_storage.endpoints.cache_statement import CacheStatementSection


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution):
        super().__init__()
        self.token = token
        self.resolution = resolution
        self.stocks = {}  # TODO : REMOVE

    def get_historical_daily_prices(self, symbol: str, start_date: date, end_date: date = None):
        """
        Gets the historical prices of the given stock for the given interval period
        Args:
            symbol: Symbol of the stock/forex
            start_date: Starting time of the interval of historical prices
            end_date: Ending time of the interval of historical price. Default value is the time of the backtest
        Returns: An array of the closing price of the stock for every day between the interval
        """
        # TODO : CHANGE THIS FUNCTION, IT DOES NOT RESPECT OUR STANDARDS
        if end_date is None:
            end_date = self.timestamp.date()

        if symbol not in self.stocks:
            self._store_price_points(symbol, start_date, end_date)
        else:
            stock = self.stocks[symbol]

            # This makes sure we're not querying price points we already have.
            if stock.start_date is not None and stock.start_date > start_date:
                uncached_start_date = start_date
                uncached_end_date = stock.start_date
                self._store_price_points(symbol, uncached_start_date, uncached_end_date)

            if stock.end_date is not None and stock.end_date < end_date:
                uncached_end_date = end_date
                uncached_start_date = stock.end_date
                self._store_price_points(symbol, uncached_start_date, uncached_end_date)

        return [p for p in self.stocks[symbol].price_points.values()
                if start_date <= datetime.strptime(p.date, "%Y-%m-%d").date() <= end_date]

    def get_price(self, symbol: str, timestamp: datetime = None, value: str = None) -> int:
        """
        Gets the price of the stock/forex at the current timestamp
        Args:
            symbol: Symbol of the stock/forex
            timestamp: Time of the data you want. If you want the current time of the backtest, leave empty
            value: Value of the stock you want (open, close, low, high, etc)
        Returns: The stock price at the given timestamp
        """
        if timestamp is None:
            wanted_date = self.timestamp
        else:
            wanted_date = timestamp

        cached_value = get_data_in_cache(CacheEndpoint.PRICE, self.resolution.name, symbol, wanted_date, value)

        if cached_value is None:
            self._store_price_points(symbol, wanted_date.date())
            return get_data_in_cache(CacheEndpoint.PRICE, self.resolution.name, symbol, wanted_date, value)
        else:
            return cached_value

    def get_income_statement(self, symbol: str, timestamp: date = None) -> IncomeStatement:
        """
        Gets the income statement of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want. If you want the current time of the backtest, leave empty
        Returns: The stock income statement at the given timestamp
        """
        if timestamp is None:
            wanted_date = self.timestamp
        else:
            wanted_date = timestamp

        cached_value = get_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.INCOME.value, symbol,
                                         wanted_date, None)

        if cached_value is None:
            self._store_income_statements(symbol)
            return get_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.INCOME.value, symbol, wanted_date,
                                     None)
        else:
            return cached_value

    def get_balance_sheet_statement(self, symbol: str, timestamp: date = None) -> BalanceSheetStatement:
        """
        Gets the balance sheet statement of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want. If you want the current time of the backtest, leave empty
        Returns: The stock balance sheet statement at the given timestamp
        """
        if timestamp is None:
            wanted_date = self.timestamp
        else:
            wanted_date = timestamp

        cached_value = get_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.BALANCE_SHEET.value, symbol,
                                         wanted_date, None)

        if cached_value is None:
            self._store_balance_sheet_statements(symbol)
            return get_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.BALANCE_SHEET.value, symbol,
                                     wanted_date, None)
        else:
            return cached_value

    def get_cash_flow_statement(self, symbol: str, timestamp: date = None) -> CashFlowStatement:
        """
        Gets the cash flow statement of the stock at the current timestamp
        Args:
            symbol: Symbol of the stock
            timestamp: Time of the data you want. If you want the current time of the backtest, leave empty
        Returns: The stock cash flow statement at the given timestamp
        """
        if timestamp is None:
            wanted_date = self.timestamp
        else:
            wanted_date = timestamp

        cached_value = get_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.CASH_FLOW.value, symbol,
                                         wanted_date, None)

        if cached_value is None:
            self._store_cash_flow_statements(symbol)
            return get_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.CASH_FLOW.value, symbol,
                                     wanted_date, None)
        else:
            return cached_value

    def get_symbol_list(self) -> list:
        """
        Gets all the symbols available in FMP
        Returns: A list (symbol, name, price, exchange) of all available symbols
        """
        url = self.URL_BASE_FMP + "stock/list?apikey=" + self.token
        response = self.request(url)
        return json.loads(response)

    def get_income_statement_list(self) -> list:
        """
        Gets all the symbols with income statements available in FMP
        Returns: A list (symbol) of all the symbols with available income statements
        """
        url = self.URL_BASE_FMP + "financial-statement-symbol-lists?apikey=" + self.token
        response = self.request(url)
        return json.loads(response)

    def get_tradable_symbol_list(self) -> list:
        """
        Gets all the tradable symbols available in FMP
        Returns: A list (symbol, name, price, exchange, exchangeShortName) of all tradable symbols
        """
        url = self.URL_BASE_FMP + "available-traded/list?apikey=" + self.token
        response = self.request(url)
        return json.loads(response)

    def get_forex_currency_pairs_list(self) -> list:
        """
        Gets all the forex currency pairs available in FMP
        Returns: A list (symbol, name, currency, stockExchange, exchangeShortName) of all available currency pairs
        """
        url = self.URL_BASE_FMP + "symbol/available-forex-currency-pairs?apikey=" + self.token
        response = self.request(url)
        return json.loads(response)

    def get_remaining_calls(self) -> int:
        """
        Gets the amount of remaining calls from the fmp datasource, this number comes directly from fmp and is not
        managed on BullETS side
        Returns: The amount of remaining FMP calls
        """
        body = {'data': {'key': self.token}}
        response = self.request(url="https://europe-west1-fmpdev-1d3ca.cloudfunctions.net/getRemainingCalls",
                                method="POST", body=body)

        return int(json.loads(response)['result'])

    def _store_price_points(self, symbol: str, start_date: datetime.date, end_date: datetime.date = None,
                            limit: int = None):

        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value) + "/"

        if limit is None:
            if self.resolution == Resolution.DAILY:
                limit = 10
            if self.resolution == Resolution.HOURLY:
                limit = 1
            elif self.resolution == Resolution.MINUTE:
                limit = 1

        if end_date is None:
            end_date = start_date + timedelta(days=limit)
            if end_date > date.today():
                end_date = date.today()

        current_end_date = end_date
        finished = False

        if start_date > date.today():
            finished = True

        while not finished:
            interval = "from=" + str(start_date) + "&to=" + str(current_end_date)
            url = self.URL_BASE_FMP + url_resolution + symbol + "?" + interval + "&apikey=" + self.token
            response = self.request(url)

            if response == "{ }" or response is None:
                break

            store_data_in_cache(CacheEndpoint.PRICE, self.resolution.name, symbol, response)
            result = json.loads(response)

            if self.resolution == Resolution.DAILY:
                data = result["historical"]
            else:
                data = result

            last_price_point = PricePoint(data[len(data) - 1])

            if self.resolution == Resolution.DAILY:
                last_price_point_date = datetime.strptime(last_price_point.date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            else:
                last_price_point_date = datetime.strptime(last_price_point.date, "%Y-%m-%d %H:%M:%S")

            if last_price_point_date.date() <= start_date or last_price_point_date.date() == current_end_date:
                finished = True
            else:
                current_end_date = last_price_point_date.date()

    def _store_income_statements(self, symbol: str):

        url = self.URL_BASE_FMP + "income-statement/" + symbol + "?apikey=" + self.token
        response = self.request(url)
        store_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.INCOME.value, symbol, response)

    def _store_balance_sheet_statements(self, symbol: str):

        url = self.URL_BASE_FMP + "balance-sheet-statement/" + symbol + "?apikey=" + self.token
        response = self.request(url)
        store_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.BALANCE_SHEET.value, symbol, response)

    def _store_cash_flow_statements(self, symbol: str):

        url = self.URL_BASE_FMP + "cash-flow-statement/" + symbol + "?apikey=" + self.token
        response = self.request(url)
        store_data_in_cache(CacheEndpoint.STATEMENT, CacheStatementSection.CASH_FLOW.value, symbol, response)
