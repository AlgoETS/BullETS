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
    logger.suppress_logs()
    runner = Runner(strategy)
    runner.start()

    def test_strategy_start_balance(self):
        self.assertEqual(5000, self.strategy.portfolio.start_balance)

    def test_strategy_final_balance(self):
        self.assertEqual(5458.0374725, self.strategy.portfolio.update_and_get_balance())

    def test_strategy_final_cash_balance(self):
        self.assertEqual(89.12497250000004, self.strategy.portfolio.cash_balance)

    def test_strategy_final_percentage_profit(self):
        self.assertEqual(9.16, self.strategy.portfolio.get_percentage_profit())

    def test_strategy_final_transaction_count(self):
        self.assertEqual(33, len(self.strategy.portfolio.transactions))

    def test_strategy_none_date(self):
        self.assertRaisesRegex(TypeError, "Invalid strategy date type", ActualStrategy,
                               self.RESOLUTION, None, None, self.STARTING_BALANCE,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_strategy_invalid_date(self):
        self.assertRaisesRegex(ValueError, "Strategy start time has to be before end time", ActualStrategy,
                               self.RESOLUTION, self.END_TIME, self.START_TIME, self.STARTING_BALANCE,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_strategy_none_resolution(self):
        self.assertRaisesRegex(TypeError, "Invalid strategy resolution type", ActualStrategy,
                               None, self.START_TIME, self.END_TIME, self.STARTING_BALANCE,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_strategy_none_data_source(self):
        self.assertRaisesRegex(TypeError, "Invalid strategy data source type", ActualStrategy,
                               self.RESOLUTION, self.START_TIME, self.END_TIME, self.STARTING_BALANCE, None)

    def test_strategy_invalid_balance(self):
        self.assertRaisesRegex(ValueError, "Strategy starting balance should be positive", ActualStrategy,
                               self.RESOLUTION, self.START_TIME, self.END_TIME, self.STARTING_BALANCE * -1,
                               FmpDataSource(self.FMP_TOKEN, self.RESOLUTION))

    def test_income_statements(self):
        datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
        self.assertEqual(2.9925, datasource.get_income_statement("AAPL", date(2019, 9, 28)).eps)

    def test_balance_sheet_statements(self):
        datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
        self.assertEqual(4106000000, datasource.get_balance_sheet_statement("AAPL", date(2019, 9, 28)).inventory)

    def test_cash_flow_statements(self):
        datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
        self.assertEqual(55256000000, datasource.get_cash_flow_statement("AAPL", date(2019, 9, 28)).net_income)

    def test_symbol_list(self):
        datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
        self.assertEqual(True, any(item['symbol'] == 'AAPL' for item in datasource.get_symbol_list()))

    def test_income_statement_list(self):
        datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
        self.assertEqual(True, 'AAPL' in datasource.get_income_statement_list())

    def test_tradable_symbol_list(self):
        datasource = FmpDataSource(self.FMP_TOKEN, self.RESOLUTION)
        self.assertEqual(True, any(item['symbol'] == 'AAPL' for item in datasource.get_tradable_symbol_list()))


if __name__ == '__main__':
    unittest.main()
