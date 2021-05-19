from bullets.fmp.historicalPrice import *
import datetime as dt

APIkey = '090bebac8a76a19401c9bb5561482a2c'
resolution = "5min"
company = "AAPL"
date = str(dt.date(2021, 5, 13))
time = str(dt.time(12, 55, 0))


class TestHistoricalPrice:
    def test_get_data(self):
        me = Client(APIkey)
        apple = Ticker(company, resolution)
        fmp = HistoricalPrice(me)
        fmp.load_data(apple)
        apple.set_date(date, time)
        print(apple.low)


test = TestHistoricalPrice()
test.test_get_data()
