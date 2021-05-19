from bullets.fmp.historicalPrice import *
from bullets.resolution import *
import datetime as dt

APIkey = '090bebac8a76a19401c9bb5561482a2c'
resolution = Resolution.daily
company = "AAPL"
date = str(dt.date(2019, 1, 23))# + " " + str(dt.time(12, 45, 0))
start_date = str(dt.date(2018, 6, 18))
end_date = str(dt.date(2020, 6, 18))


class TestHistoricalPrice:
    def test_get_data(self):
        me = Client(APIkey)
        apple = Stock(company, resolution)
        fmp = HistoricalPrice(me)

        fmp.load_data(apple, start_date, end_date)
        print(apple.ticker(date).price)


test = TestHistoricalPrice()
test.test_get_data()
