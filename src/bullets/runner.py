from datetime import datetime, timedelta
from bullets.portfolio.transaction import Status
from bullets.strategy import Strategy
from bullets.data_source.data_source_interface import Resolution
from bullets.data_source.data_source_fmp import FmpDataSource
from bullets import logger
from bullets.utils.holiday_date_util import us_holiday_list
import os
import os.path as osp
import json

class Runner:
    def __init__(self, strategy: Strategy, logdir: str = None):
        self.strategy = strategy
        self.logdir = logdir
        self.holidays = None
        self.stats = {}

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
        self._post_backtest_log()

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

    def _post_backtest_log(self):
        self._update_final_timestamp()
        logger.info("=========== Backtest complete ===========")
        logger.info("Initial Cash : " + str(self.strategy.starting_balance))
        logger.info("Final Balance : " + str(self.strategy.portfolio.update_and_get_balance()))
        logger.info("Final Cash : " + str(self.strategy.portfolio.cash_balance))
        logger.info("Profit : " + str(self.strategy.portfolio.get_percentage_profit()) + "%")
        if isinstance(self.strategy.data_source, FmpDataSource):
            logger.info("Remaining FMP Calls :  " + str(self.strategy.data_source.get_remaining_calls()))
        if not self.logdir is None:
            self._save_final_stats()

    def _update_final_timestamp(self):
        final_timestamp = self.strategy.start_time
        for transaction in self.strategy.portfolio.transactions:
            if transaction.status != Status.FAILED_SYMBOL_NOT_FOUND and transaction.timestamp > final_timestamp:
                final_timestamp = transaction.timestamp
        self.strategy.update_time(final_timestamp)

    def _save_final_stats(self):
        self.stats['profit'] = self.strategy.portfolio.cash_balance - self.strategy.starting_balance
        self.stats['final_balance'] = self.strategy.portfolio.cash_balance
        self.stats['starting_balance'] = self.strategy.starting_balance
        self.stats['user_statistics'] = self.strategy._strategy_statistics

        LOG_REPO = "../log" #TODO : put in env file
        print(os.getcwd())
        try:
            original_umask = os.umask(0)
            os.makedirs(osp.join(LOG_REPO, self.logdir), mode=0o777)
        except OSError as error:
            print(error)
        finally:
            os.umask(original_umask)

        #TODO : add a temporary csv format save so the report can be handled with excel as well
        with open(osp.join(LOG_REPO,self.logdir,'strategy_report.json'), 'w', encoding='utf-8') as fp:
            json.dump(self.stats, fp, indent=4,ensure_ascii=False,)
        print("Log file successfully saved under {}".format(osp.join(LOG_REPO, self.logdir)))
        return 0
