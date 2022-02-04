import csv
import sys
from datetime import datetime, timedelta
from bullets.portfolio.transaction import Status
from bullets.strategy import Strategy
from bullets.data_source.data_source_interface import Resolution
from bullets.data_source.data_source_fmp import FmpDataSource
from bullets import logger
from bullets.utils.holiday_date_util import us_holiday_list
import os

from streamlit import cli as stcli


class Runner:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.holidays = None

    def start(self):
        """
        Starts running the backtest
        """
        if self.strategy is None:
            raise TypeError("No strategy was attached to the runner.")
        logger.info("=========== Backtest started ===========")
        moments = self._get_moments(self.strategy.resolution, self.strategy.start_time, self.strategy.end_time)
        self.strategy.update_time(moments[0])
        self.strategy.on_start()
        for moment in moments:
            self.strategy.update_time(moment)
            self.strategy.on_resolution()
            self.strategy.portfolio.on_resolution()
        self.strategy.on_finish()
        logger.info("=========== Backtest complete ===========")
        self._save_backtest_log()
        self._open_viewer_app()

    def _get_moments(self, resolution: Resolution, start_time: datetime, end_time: datetime):
        moments = []
        current_time = start_time

        while current_time != end_time:
            if resolution == Resolution.DAILY:
                current_time = current_time + timedelta(days=1)
            elif resolution == Resolution.HOURLY:
                current_time = current_time + timedelta(hours=1)
            elif resolution == Resolution.MINUTE:
                current_time = current_time + timedelta(minutes=1)

            if self._is_market_open(current_time, resolution):
                moments.append(current_time)

        return moments

    @staticmethod
    def _is_market_open(date: datetime, resolution: Resolution) -> bool:
        if date.weekday() >= 5:
            return False

        if resolution != Resolution.DAILY:
            if date.hour < 9 or date.hour > 16:
                return False
            elif date.hour == 16 and date.minute > 0:
                return False
            elif date.hour == 9 and date.minute < 30:
                return False

        return date not in us_holiday_list(date.year)

    def _save_backtest_log(self):
        new_dir = self.strategy.output_folder + datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        os.mkdir(new_dir)
        self._save_stats_to_csv(new_dir + "/Stats.csv")
        self._save_transactions_to_csv(new_dir + "/Transactions.csv")

    def _save_stats_to_csv(self, file: str):
        with open(file, 'w', newline='', encoding='utf-8') as outputFile:
            writer = csv.writer(outputFile, delimiter=';')
            writer.writerow(["Initial Cash", self.strategy.starting_balance])
            writer.writerow(["Final Balance", self.strategy.portfolio.update_and_get_balance()])
            writer.writerow(["Final Cash", self.strategy.portfolio.cash_balance])
            writer.writerow(["Profit", str(self.strategy.portfolio.get_percentage_profit()) + "%"])
            if isinstance(self.strategy.data_source, FmpDataSource):
                writer.writerow(["Remaining FMP Calls", self.strategy.data_source.get_remaining_calls()])
        logger.info("Stats sheet saved to : " + file)

    def _save_transactions_to_csv(self, file: str):
        with open(file, 'w', newline='', encoding='utf-8') as outputFile:
            writer = csv.writer(outputFile, delimiter=';')
            headers = ['Status', 'Order Type', 'Time', 'Symbol', 'Share Count', 'Simulated Price', 'Total Price',
                       'Cash Balance']
            writer.writerow(headers)
            for tr in self.strategy.portfolio.transactions:
                writer.writerow([tr.status.value, tr.order_type, tr.timestamp, tr.symbol, tr.nb_shares,
                                 tr.simulated_price, tr.total_price, tr.cash_balance])
        logger.info("Transactions sheet saved to : " + file)

    def _update_final_timestamp(self):
        final_timestamp = self.strategy.start_time
        for transaction in self.strategy.portfolio.transactions:
            if transaction.status != Status.FAILED_SYMBOL_NOT_FOUND and transaction.timestamp > final_timestamp:
                final_timestamp = transaction.timestamp
        self.strategy.update_time(final_timestamp)

    def _open_viewer_app(self):
        # TODO : Open the viewer app and make it visualise the data stored in the files
        #        (see _save_stats_to_csv & _save_transactions_to_cvs)
        #
        sys.argv = ["streamlit", "run", "..\\bullets\\viewer\\viewer_app.py"]
        stcli.main()
