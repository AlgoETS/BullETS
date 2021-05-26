from bullets.fmp.historicalPrice import *
from bullets.fmp.incomeStatements import *
from bullets.resolution import *
import datetime as dt

APIkey = '090bebac8a76a19401c9bb5561482a2c'
resolution = Resolution.Min30
company = "AAPL"
date = str(dt.date(2018, 3, 15)) + " " + str(dt.time(11, 0, 0))
start_date = str(dt.date(2018, 3, 12))
end_date = str(dt.date(2019, 3, 12))


class TestHistoricalPrice:
    def test_get_data(self):
        me = Client(APIkey)
        apple = Stock(company, resolution)
        fmp = HistoricalPrice(me)

        fmp.load_data(apple, start_date, end_date)
        print(apple.get_ticker(date).open)


test = TestHistoricalPrice()
test.test_get_data()
