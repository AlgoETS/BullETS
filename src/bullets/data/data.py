from datetime import datetime
from bullets.strategy import Resolution


### TO BE MOVED IN A BASE CLASS ###
class HistoricalPrice:
    def __init__(self, ticker: str, date_time: datetime, price: float):
        self.ticker = ticker
        self.date_time = date_time
        self.price = price


class BaseData:
    def __init__(self, ticker: str, start_time: datetime, end_time: datetime, client: client):
        self.ticker = ticker
        self.start_time = start_time
        self.end_time = end_time
        self.client = client

    def get_daily_historical_price(self):
        indicators = []
        resolution_count = 5  # TEMP

        if Resolution == Resolution.DAILY:
            for x in range(resolution_count):
                indicators.append(HistoricalPrice("AAPL", datetime(2020, 1, x + 1), x + 100))

            return indicators
        else:
            raise Exception("NOT IMPLEMENTED YET.")