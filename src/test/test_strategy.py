import os
import unittest

from bullets import logger
from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from bullets.data_source.data_source_fmp import FmpDataSource
from datetime import datetime, date


class ActualStrategy(Strategy):
    def on_start(self):
        pass

    def on_resolution(self):
        self.portfolio.market_order("AAPL", 5)

    def on_finish(self):
        pass


class TestStrategy(unittest.TestCase):
    RESOLUTION = Resolution.DAILY
    START_TIME = datetime(2019, 3, 5)
    END_TIME = datetime(2019, 4, 22)
    STARTING_BALANCE = 5000
    FMP_TOKEN = os.getenv("FMP_TOKEN")
    strategy = ActualStrategy(resolution=RESOLUTION,
                              start_time=START_TIME,
                              end_time=END_TIME,
                              starting_balance=STARTING_BALANCE,
                              data_source=FmpDataSource(FMP_TOKEN, RESOLUTION))
    logger.set_log_level("WARNING")
    runner = Runner(strategy)
    runner.start()
    logger.set_log_level("INFO")

    def test_strategy_start_balance(self):
        try:
            self.assertEqual(5000, self.strategy.portfolio.start_balance)
            logger.info("Strategy start balance test successful")
        finally:
            pass

    def test_strategy_final_investment_balance(self):
        try:
            self.assertEqual(5458.0374725, self.strategy.portfolio.update_and_get_balance())
            logger.info("Strategy final investment balance test successful")
        finally:
            pass

    def test_strategy_final_cash_balance(self):
        try:
            self.assertEqual(89.12497250000004, self.strategy.portfolio.cash_balance)
            logger.info("Strategy final cash balance test successful")
        finally:
            pass

    def test_strategy_final_percentage_profit(self):
        try:
            self.assertEqual(9.16, self.strategy.portfolio.get_percentage_profit())
            logger.info("Strategy final percentage profit test successful")
        finally:
            pass

    def test_strategy_final_transaction_count(self):
        try:
            self.assertEqual(33, len(self.strategy.portfolio.transactions))
            logger.info("Strategy final transaction count test successful")
        finally:
            pass

    def test_strategy_none_date(self):
        try:
            self.assertRaisesRegex(TypeError, "Invalid strategy date type", ActualStrategy,
                                   self.RESOLUTION, None, None, self.STARTING_BALANCE,
                                   FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))
            logger.info("Invalid strategy date type test successful")
        finally:
            pass

    def test_strategy_invalid_date(self):
        try:
            self.assertRaisesRegex(ValueError, "Strategy start time has to be before end time", ActualStrategy,
                                   self.RESOLUTION, self.END_TIME, self.START_TIME, self.STARTING_BALANCE,
                                   FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))
            logger.info("Invalid strategy start time & end time test successful")
        finally:
            pass

    def test_strategy_none_resolution(self):
        try:
            self.assertRaisesRegex(TypeError, "Invalid strategy resolution type", ActualStrategy,
                                   None, self.START_TIME, self.END_TIME, self.STARTING_BALANCE,
                                   FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))
            logger.info("Invalid strategy resolution type test successful")
        finally:
            pass

    def test_strategy_none_data_source(self):
        try:
            self.assertRaisesRegex(TypeError, "Invalid strategy data source type", ActualStrategy,
                                   self.RESOLUTION, self.START_TIME, self.END_TIME, self.STARTING_BALANCE, None)
            logger.info("Invalid strategy data source test successful")
        finally:
            pass

    def test_strategy_invalid_balance(self):
        try:
            self.assertRaisesRegex(ValueError, "Strategy starting balance should be positive", ActualStrategy,
                                   self.RESOLUTION, self.START_TIME, self.END_TIME, self.STARTING_BALANCE * -1,
                                   FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))
            logger.info("Invalid strategy balance test successful")
        finally:
            pass

    def test_income_statement(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(2.9925, datasource.get_income_statement("AAPL", date(2019, 9, 28)).eps)
            logger.info("Income statement test successful")
        finally:
            pass

    def test_income_statement_list(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(True, 'AAPL' in datasource.get_income_statement_list())
            logger.info("Income statement list test successful")
        finally:
            pass

    def test_balance_sheet_statements(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(4106000000, datasource.get_balance_sheet_statement("AAPL", date(2019, 9, 28)).inventory)
            logger.info("Balance sheet statements test successful")
        finally:
            pass

    def test_cash_flow_statements(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(55256000000, datasource.get_cash_flow_statement("AAPL", date(2019, 9, 28)).net_income)
            logger.info("Cash flow statements test successful")
        finally:
            pass

    def test_symbol_list(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(True, any(item['symbol'] == 'AAPL' for item in datasource.get_symbol_list()))
            logger.info("Symbol list test successful")
        finally:
            pass

    def test_forex_currency_pairs_list(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(True, any(item['symbol'] == 'JPYUSD' for item in datasource.get_forex_currency_pairs_list()))
            logger.info("Forex currency pairs list test successful")
        finally:
            pass

    def test_tradable_symbol_list(self):
        try:
            datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
            self.assertEqual(True, any(item['symbol'] == 'AAPL' for item in datasource.get_tradable_symbol_list()))
            logger.info("Tradable symbol list test successful")
        finally:
            pass


if __name__ == '__main__':
    unittest.main()
