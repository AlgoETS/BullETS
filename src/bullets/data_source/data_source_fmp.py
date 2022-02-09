import json
import math
from datetime import datetime, date, timedelta
from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets.data_source.recorded_data import *


class FmpDataSource(DataSourceInterface):
    URL_BASE_FMP = 'https://financialmodelingprep.com/api/v3/'

    def __init__(self, token: str, resolution: Resolution):
        super().__init__()
        self.token = token
        self.resolution = resolution
        self.stocks = {}

    def get_historical_daily_prices(self, symbol: str, start_date: date, end_date: date = None):
        """
        Gets the historical prices of the given stock for the given interval period
        Args:
            symbol: Symbol of the stock/forex
            start_date: Starting time of the interval of historical prices
            end_date: Ending time of the interval of historical price. Default value is the time of the backtest
        Returns: An array of the closing price of the stock for every day between the interval
        """
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

        already_cached = self._get_cached_price(symbol, wanted_date, value)

        if already_cached is None:
            self._store_price_points(symbol, wanted_date.date())
            newly_cached = self._get_cached_price(symbol, wanted_date, value)
            if newly_cached is None:
                return None
            else:
                return newly_cached
        else:
            return already_cached

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

        already_cached = self._get_cached_income_statement(symbol, wanted_date)

        if already_cached is None:
            self._store_income_statements(symbol)
            newly_cached = self._get_cached_income_statement(symbol, wanted_date)
            if newly_cached is None:
                return None
            else:
                return newly_cached
        else:
            return already_cached

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

        already_cached = self._get_cached_balance_sheet_statement(symbol, wanted_date)

        if already_cached is None:
            self._store_balance_sheet_statements(symbol)
            newly_cached = self._get_cached_balance_sheet_statement(symbol, wanted_date)
            if newly_cached is None:
                return None
            else:
                return newly_cached
        else:
            return already_cached

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

        already_cached = self._get_cached_cash_flow_statement(symbol, wanted_date)

        if already_cached is None:
            self._store_cash_flow_statements(symbol)
            newly_cached = self._get_cached_cash_flow_statement(symbol, wanted_date)
            if newly_cached is None:
                return None
            else:
                return newly_cached
        else:
            return already_cached

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

    def _get_cached_price(self, symbol: str, wanted_date: datetime, value: str):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
            if wanted_date in stock.price_points:
                return self._get_specific_price_value(wanted_date, stock, value)

    def _get_cached_income_statement(self, symbol: str, wanted_date: date):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
            if wanted_date in stock.income_statements:
                return stock.income_statements[wanted_date]

    def _get_cached_balance_sheet_statement(self, symbol: str, wanted_date: date):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
            if wanted_date in stock.balance_sheet_statements:
                return stock.balance_sheet_statements[wanted_date]

    def _get_cached_cash_flow_statement(self, symbol: str, wanted_date: date):
        if symbol in self.stocks:
            stock = self.stocks[symbol]
            if wanted_date in stock.cash_flow_statements:
                return stock.cash_flow_statements[wanted_date]

    def _store_price_points(self, symbol: str, start_date: datetime.date, end_date: datetime.date = None,
                            limit: int = 1000):
        stock = self._get_or_create_stock(symbol)

        if self.resolution == Resolution.DAILY:
            url_resolution = "historical-price-full/"
        else:
            url_resolution = "historical-chart/" + str(self.resolution.value) + "/"

        if end_date is None:
            nb_entree = limit
            if self.resolution == Resolution.HOURLY:
                nb_entree = math.ceil(nb_entree / 6)
            elif self.resolution == Resolution.MINUTE:
                nb_entree = math.ceil(nb_entree / 390)

            end_date = start_date + timedelta(days=nb_entree)
            if end_date > date.today():
                end_date = date.today()

        current_end_date = end_date
        finished = False

        while not finished:
            interval = "from=" + str(start_date) + "&to=" + str(current_end_date)
            url = self.URL_BASE_FMP + url_resolution + symbol + "?" + interval + "&apikey=" + self.token
            response = self.request(url)

            if stock.start_date is None or stock.start_date > start_date:
                stock.start_date = start_date

            if stock.end_date is None or stock.end_date < current_end_date:
                stock.end_date = current_end_date

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
                    stock_date = datetime.strptime(price_point.date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                else:
                    stock_date = datetime.strptime(price_point.date, "%Y-%m-%d %H:%M:%S")

                stock.price_points[stock_date] = price_point
                first_date = stock_date.date()
            if current_end_date == first_date:
                finished = True
            else:
                current_end_date = first_date

            if first_date <= start_date:
                finished = True

        self.stocks[symbol] = stock

    def _store_income_statements(self, symbol: str):
        stock = self._get_or_create_stock(symbol)

        url = self.URL_BASE_FMP + "income-statement/" + symbol + "?apikey=" + self.token
        response = self.request(url)
        result = json.loads(response)

        for entry in result:
            income_statement = IncomeStatement(entry)
            income_statement_date = datetime.strptime(income_statement.date, "%Y-%m-%d").date()
            stock.income_statements[income_statement_date] = income_statement

        self.stocks[symbol] = stock

    def _store_balance_sheet_statements(self, symbol: str):
        stock = self._get_or_create_stock(symbol)

        url = self.URL_BASE_FMP + "balance-sheet-statement/" + symbol + "?apikey=" + self.token
        response = self.request(url)
        result = json.loads(response)

        for entry in result:
            balance_sheet_statement = BalanceSheetStatement(entry)
            balance_sheet_statement_date = datetime.strptime(balance_sheet_statement.date, "%Y-%m-%d").date()
            stock.balance_sheet_statements[balance_sheet_statement_date] = balance_sheet_statement

        self.stocks[symbol] = stock

    def _store_cash_flow_statements(self, symbol: str):
        stock = self._get_or_create_stock(symbol)

        url = self.URL_BASE_FMP + "cash-flow-statement/" + symbol + "?apikey=" + self.token
        response = self.request(url)
        result = json.loads(response)

        for entry in result:
            cash_flow_statement = CashFlowStatement(entry)
            cash_flow_statement_date = datetime.strptime(cash_flow_statement.date, "%Y-%m-%d").date()
            stock.cash_flow_statements[cash_flow_statement_date] = cash_flow_statement

        self.stocks[symbol] = stock

    @staticmethod
    def _get_specific_price_value(date: datetime, stock: Stock, value: str):
        if value is None or value == "close":
            return stock.price_points[date].close
        elif value == "date":
            return stock.price_points[date].date
        elif value == "open":
            return stock.price_points[date].open
        elif value == "low":
            return stock.price_points[date].low
        elif value == "high":
            return stock.price_points[date].high
        elif value == "volume":
            return stock.price_points[date].volume

    def _get_or_create_stock(self, symbol: str) -> Stock:
        if symbol in self.stocks:
            stock = self.stocks[symbol]
        else:
            stock = Stock(symbol, self.resolution)
        return stock
