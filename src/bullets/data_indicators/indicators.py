from bullets.data_source.data_source_interface import DataSourceInterface, Resolution
from bullets.runner import Runner
from datetime import datetime, timedelta

class Indicators:

    @staticmethod
    def simple_moving_avg(data_source: DataSourceInterface, symbol: str, target_date: datetime, days: int):
        """
        Calculates the Simple Moving Average
        Args:
            data_source: current data source
            symbol: Stock symbol
            target_date: Date of average / start date
            days: number of days for the average
        Returns:
            sma: Average stock price for the given range
        """
        ##TODO try with getting first
        data_source.get_price(symbol=symbol, timestamp=(target_date - timedelta(days=days)))

        values = []

        for x in range(days):
            #Make sure market is open
            while not Runner._is_market_open(target_date, Resolution.DAILY):
                target_date - timedelta(days=1)

            #Fetch stock value
            values.append(data_source.get_price(symbol=symbol, timestamp=target_date))

            ##Go back one day
            target_date - timedelta(days=1)

        #Calculate SMA
        sma = sum(values) / len(values)

        return sma
