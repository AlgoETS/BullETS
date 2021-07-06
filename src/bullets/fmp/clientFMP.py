# Data provided by Financial Modeling Prep
from bullets.dataStorage.balanceSheet import BalanceSheet
from bullets.dataStorage.cashFlow import CashFlow
from bullets.dataStorage.incomeStatement import IncomeStatement
from bullets.dataStorage.stock import *
from bullets.fmp.apiType import ApiType
from bullets.fmp.apiCall import ApiCall
from bullets.resolution import *
from bullets.client import Client
from datetime import date, datetime
import asyncio
import json


class ClientFMP(Client):
    def __init__(self, token: str):
        super().__init__(token)
        self.api_call = ApiCall(token)

    def load_historical_price(self, stock: Stock, start_date: date, end_date: date):
        self.api_call.type = ApiType.HistoricalPrice
        key_date = date(1, 1, 1)
        finished = False
        while not finished:
            url = self.api_call.get_data(stock.symbol, resolution=stock.resolution,
                                         start_date=start_date, end_date=end_date)
            result = json.loads(asyncio.get_event_loop().run_until_complete(self.request(url)))

            if stock.resolution == Resolution.Daily:
                data = result["historical"]
            else:
                data = result

            for entry in data:
                entry_date = entry["date"]

                key_date = date(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10]))

                ticker = Ticker.set_data(entry)

                if stock.resolution == Resolution.Daily:
                    stock.tickers[key_date] = ticker
                else:
                    key_datetime = datetime(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10]),
                                            int(entry_date[11:13]), int(entry_date[14:16]), int(entry_date[17:19]))
                    stock.tickers[key_datetime] = ticker

            finished = self.api_call.is_all_data_retrieved(start_date, key_date)
            end_date = key_date

    def load_company_profile(self, stock: Stock):
        self.api_call.type = ApiType.Profile
        url = self.api_call.get_data(stock.symbol)
        result = json.loads(asyncio.run(self.request(url)))[0]

        stock.mktCap = result["mktCap"]
        stock.currency = result["currency"]
        stock.exchange = result["exchangeShortName"]
        stock.sector = result["sector"]

    def load_income_statement(self, stock: Stock, timespan=Timespan.Yearly):
        self.api_call.type = ApiType.IncomeStatement
        url = self.api_call.get_data(stock.symbol, timespan=timespan)
        result = json.loads(asyncio.run(self.request(url)))

        for entry in result:
            entry_date = entry["date"]
            period = entry["period"]
            key = entry_date[0:4] + " " + period
            stock.income_statement[key] = IncomeStatement(entry)

    def load_balance_sheet(self, stock: Stock, timespan=Timespan.Yearly):
        self.api_call.type = ApiType.BalanceSheet
        url = self.api_call.get_data(stock.symbol, timespan=timespan)
        result = json.loads(asyncio.run(self.request(url)))

        for entry in result:
            entry_date = entry["date"]
            period = entry["period"]
            key = entry_date[0:4] + " " + period
            stock.balance_sheet[key] = BalanceSheet(entry)

    def load_cash_flow(self, stock: Stock, timespan=Timespan.Yearly):
        self.api_call.type = ApiType.CashFlow
        url = self.api_call.get_data(stock.symbol, timespan=timespan)
        result = json.loads(asyncio.run(self.request(url)))

        for entry in result:
            entry_date = entry["date"]
            period = entry["period"]
            key = entry_date[0:4] + " " + period
            stock.cash_flow[key] = CashFlow(entry)
