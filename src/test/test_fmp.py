from bullets.dataStorage.stock import *
from bullets.fmp.clientFMP import ClientFMP
from bullets.resolution import *
import datetime as dt

APIkey = '090bebac8a76a19401c9bb5561482a2c'
resolution = Resolution.Min30
company = "AAPL"
date = dt.datetime(2018, 3, 15, 10, 30, 0)
start_date = dt.date(2018, 3, 12)
end_date = dt.date(2019, 3, 12)


class TestFMP:
    def test_get_data(self):
        me = ClientFMP(APIkey)
        apple = Stock(company, resolution)

        me.load_historical_price(apple, start_date, end_date)
        print(apple.get_ticker(date).open)
        #
        # me.load_balance_sheet(apple, Timespan.Quarterly)
        # print(apple.get_statement("b", 2019, "Q2").assets.non_current_total)
        #
        # me.load_income_statement(apple)
        # print(apple.get_statement("i", 2019).expenses.research_development)


test = TestFMP()
test.test_get_data()
