import json
from datetime import datetime
from enum import Enum

from bullets.data_source.recorded_data import IncomeStatement, BalanceSheetStatement, CashFlowStatement
from bullets.data_storage.endpoints.cache_interface import CacheInterface


class CacheStatementSection(Enum):
    INCOME = "INCOME"
    BALANCE_SHEET = "BALANCE-SHEET"
    CASH_FLOW = "CASH-FLOW"


class CacheStatement(CacheInterface):
    @staticmethod
    def get_data(section: str, file: str, timestamp: str, value: str):
        with open(file, "r") as data_file:
            data = json.load(data_file)

        for entry in data:
            recorded_data = _create_recorded_data_from_entry(entry, section)
            if entry["date"] == timestamp.strftime("%Y-%m-%d"):
                return recorded_data
        return None

    @staticmethod
    def post_data(section: str, data: str, file: bytes):
        with open(file, "w") as output_file:
            output_file.write(data)

    @staticmethod
    def merge_data(section: str, new_data: str, file: bytes):
        with open(file, "r") as cache_file:
            old_data = json.load(cache_file)

        new_data_json = json.loads(new_data)

        for entry in new_data_json:
            if entry not in old_data:
                old_data.append(entry)

        with open(file, "w") as cache_file:
            json.dump(old_data, cache_file, indent=1)


def _create_recorded_data_from_entry(entry: str, section: str):
    if section == CacheStatementSection.INCOME.value:
        return IncomeStatement(entry)
    elif section == CacheStatementSection.BALANCE_SHEET.value:
        return BalanceSheetStatement(entry)
    elif section == CacheStatementSection.CASH_FLOW.value:
        return CashFlowStatement(entry)
    pass
