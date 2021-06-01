

class CashFlow:
    __slots__ = ["net_income", "depreciation_amortization", "deferred_income_tax", "accounts_receivables",
                 "stock_based_compensation", "change_working_capital", "inventory", "accounts_payables",
                 "other_working_capital", "other_non_cash_items", "net_cash_by_operating_activities",
                 "net_cash_for_investing_activities", "net_cash_financing_activities",
                 "investments_property_equipment", "net_acquisitions", "purchases_investments",
                 "sales_maturities_investments", "other_investing_activities", "dept_repayment",
                 "common_stock_issued", "common_stock_repurchased", "dividends_paid",
                 "other_financing_activities", "effect_forex_cash_changes", "net_change_in_cash",
                 "cash_end_period", "cash_beginning_period", "operating_cash_flow",
                 "capital_expenditure", "free_cash_flow"]

    def __init__(self, data: dict):
        """
        Initializes the required variable for the IncomeStatement

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        self.net_income = data["netIncome"]
        self.depreciation_amortization = data["depreciationAndAmortization"]
        self.deferred_income_tax = data["deferredIncomeTax"]
        self.accounts_receivables = data["accountsReceivables"]
        self.stock_based_compensation = data["stockBasedCompensation"]
        self.change_working_capital = data["changeInWorkingCapital"]
        self.inventory = data["inventory"]
        self.accounts_payables = data["accountsPayables"]
        self.other_working_capital = data["otherWorkingCapital"]
        self.other_non_cash_items = data["otherNonCashItems"]
        self.net_cash_by_operating_activities = data["netCashProvidedByOperatingActivities"]
        self.net_cash_for_investing_activities = data["netCashUsedForInvestingActivites"] #there's a typo in the FMP data base
        self.net_cash_financing_activities = data["netCashUsedProvidedByFinancingActivities"]
        self.investments_property_equipment = data["investmentsInPropertyPlantAndEquipment"]
        self.net_acquisitions = data["acquisitionsNet"]
        self.purchases_investments = data["purchasesOfInvestments"]
        self.sales_maturities_investments = data["salesMaturitiesOfInvestments"]
        self.other_investing_activities = data["otherInvestingActivites"] #there's a typo in the FMP data base
        self.dept_repayment = data["debtRepayment"]
        self.common_stock_issued = data["commonStockIssued"]
        self.common_stock_repurchased = data["commonStockRepurchased"]
        self.dividends_paid = data["dividendsPaid"]
        self.other_financing_activities = data["otherFinancingActivites"] #there's a typo in the FMP data base
        self.effect_forex_cash_changes = data["effectOfForexChangesOnCash"]
        self.net_change_in_cash = data["netChangeInCash"]
        self.cash_end_period = data["cashAtEndOfPeriod"]
        self.cash_beginning_period = data["cashAtBeginningOfPeriod"]
        self.operating_cash_flow = data["operatingCashFlow"]
        self.capital_expenditure = data["capitalExpenditure"]
        self.free_cash_flow = data["freeCashFlow"]
