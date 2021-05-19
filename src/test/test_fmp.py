from bullets.fmp.historicalPrice import *
from bullets.resolution import *
import datetime as dt

APIkey = '090bebac8a76a19401c9bb5561482a2c'
resolution = Resolution.min15
company = "AAPL"
date = str(dt.date(2021, 5, 18)) + " " + str(dt.time(12, 45, 0))


class TestHistoricalPrice:
    def test_get_data(self):
        me = Client(APIkey)
        apple = Stock(company, resolution)
        fmp = HistoricalPrice(me)

        fmp.load_data(apple)
        print(apple.ticker[date].price)


test = TestHistoricalPrice()
test.test_get_data()
