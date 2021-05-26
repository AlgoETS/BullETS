from enum import Enum


class ApiType(str, Enum):
    HistoricalPrice = "historical-chart"
    Profile = "profile"
    IncomeStatement = "income-statement"
    BalanceSheet = "balance-sheet-statement"
    CashFlow = "cash-flow-statement"

    def __str__(self):
        return self.value
