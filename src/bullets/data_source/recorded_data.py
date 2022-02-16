from datetime import datetime
from bullets.data_source.data_source_interface import Resolution


class Stock:
    def __init__(self, symbol: str, resolution: Resolution):
        self.symbol = symbol
        self.resolution = resolution
        self.price_points = {}
        self.income_statements = {}
        self.balance_sheet_statements = {}
        self.cash_flow_statements = {}
        self.start_date = None
        self.end_date = None


class PricePoint:
    def __init__(self, entry: dict):
        self.date = entry["date"]
        self.open = entry["open"]
        self.low = entry["low"]
        self.high = entry["high"]
        self.close = entry["close"]
        self.volume = entry["volume"]


class IncomeStatement:
    def __init__(self, entry: dict):
        self.date = entry["date"]
        self.reported_currency = entry["reportedCurrency"]
        self.filling_date = entry["fillingDate"]
        self.accepted_date = entry["acceptedDate"]
        self.period = entry["period"]
        self.revenue = entry["revenue"]
        self.cost_of_revenue = entry["costOfRevenue"]
        self.gross_profit = entry["grossProfit"]
        self.gross_profit_rRatio = entry["grossProfitRatio"]
        self.research_and_development_expenses = entry["researchAndDevelopmentExpenses"]
        self.general_and_administrative_expenses = entry["generalAndAdministrativeExpenses"]
        self.selling_and_marketing_expenses = entry["sellingAndMarketingExpenses"]
        self.selling_general_and_administrative_expenses = entry["sellingGeneralAndAdministrativeExpenses"]
        self.other_expenses = entry["otherExpenses"]
        self.cost_and_expenses = entry["costAndExpenses"]
        self.interest_expense = entry["interestExpense"]
        self.depreciation_and_amortization = entry["depreciationAndAmortization"]
        self.ebitda = entry["ebitda"]
        self.ebitda_ratio = entry["ebitdaratio"]
        self.operating_income = entry["operatingIncome"]
        self.operating_income_ratio = entry["operatingIncomeRatio"]
        self.total_other_income_expenses_net = entry["totalOtherIncomeExpensesNet"]
        self.income_before_tax = entry["incomeBeforeTax"]
        self.income_before_tax_ratio = entry["incomeBeforeTaxRatio"]
        self.income_tax_expense = entry["incomeTaxExpense"]
        self.net_income = entry["netIncome"]
        self.net_income_ratio = entry["netIncomeRatio"]
        self.eps = entry["eps"]
        self.eps_diluted = entry["epsdiluted"]
        self.weighted_average_shs_out = entry["weightedAverageShsOut"]
        self.weighted_average_shs_out_dil = entry["weightedAverageShsOutDil"]
        self.link = entry["link"]
        self.final_link = entry["finalLink"]


class BalanceSheetStatement:
    def __init__(self, entry: dict):
        self.date = entry["date"]
        self.reported_currency = entry["reportedCurrency"]
        self.filling_date = entry["fillingDate"]
        self.accepted_date = entry["acceptedDate"]
        self.period = entry["period"]
        self.cash_and_cash_equivalents = entry["cashAndCashEquivalents"]
        self.cash_and_short_term_investments = entry["cashAndShortTermInvestments"]
        self.net_receivables = entry["netReceivables"]
        self.inventory = entry["inventory"]
        self.other_current_assets = entry["otherCurrentAssets"]
        self.total_current_assets = entry["totalCurrentAssets"]
        self.property_plant_equipment_net = entry["propertyPlantEquipmentNet"]
        self.goodwill = entry["goodwill"]
        self.intangible_assets = entry["intangibleAssets"]
        self.goodwill_and_intangible_assets = entry["goodwillAndIntangibleAssets"]
        self.long_term_investments = entry["longTermInvestments"]
        self.tax_assets = entry["taxAssets"]
        self.other_non_current_assets = entry["otherNonCurrentAssets"]
        self.total_non_current_assets = entry["totalNonCurrentAssets"]
        self.other_assets = entry["otherAssets"]
        self.total_assets = entry["totalAssets"]
        self.account_payables = entry["accountPayables"]
        self.short_term_debt = entry["shortTermDebt"]
        self.tax_payables = entry["taxPayables"]
        self.deferred_revenue = entry["deferredRevenue"]
        self.other_current_liabilities = entry["otherCurrentLiabilities"]
        self.total_current_liabilities = entry["totalCurrentLiabilities"]
        self.long_term_debt = entry["longTermDebt"]
        self.deferred_revenue_non_current = entry["deferredRevenueNonCurrent"]
        self.deferred_tax_liabilities_non_current = entry["deferredTaxLiabilitiesNonCurrent"]
        self.other_non_current_liabilities = entry["otherNonCurrentLiabilities"]
        self.total_non_current_liabilities = entry["totalNonCurrentLiabilities"]
        self.other_liabilities = entry["otherLiabilities"]
        self.total_liabilities = entry["totalLiabilities"]
        self.common_stock = entry["commonStock"]
        self.retained_earnings = entry["retainedEarnings"]
        self.accumulated_other_comprehensive_income_loss = entry["accumulatedOtherComprehensiveIncomeLoss"]
        self.other_total_stockholders_equity = entry["othertotalStockholdersEquity"]
        self.total_stockholders_equity = entry["totalStockholdersEquity"]
        self.total_liabilities_and_stockholders_equity = entry["totalLiabilitiesAndStockholdersEquity"]
        self.total_investments = entry["totalInvestments"]
        self.total_debt = entry["totalDebt"]
        self.net_debt = entry["netDebt"]
        self.link = entry["link"]
        self.final_link = entry["finalLink"]


class CashFlowStatement:
    def __init__(self, entry: dict):
        self.date = entry["date"]
        self.reported_currency = entry["reportedCurrency"]
        self.filling_date = entry["fillingDate"]
        self.accepted_date = entry["acceptedDate"]
        self.period = entry["period"]
        self.net_income = entry["netIncome"]
        self.depreciation_and_amortization = entry["depreciationAndAmortization"]
        self.deferred_income_tax = entry["deferredIncomeTax"]
        self.stock_based_compensation = entry["stockBasedCompensation"]
        self.change_in_working_capital = entry["changeInWorkingCapital"]
        self.accounts_receivables = entry["accountsReceivables"]
        self.inventory = entry["inventory"]
        self.accounts_payables = entry["accountsPayables"]
        self.other_working_capital = entry["otherWorkingCapital"]
        self.other_non_cash_items = entry["otherNonCashItems"]
        self.net_cash_provided_by_operating_activities = entry["netCashProvidedByOperatingActivities"]
        self.investments_in_property_plant_and_equipment = entry["investmentsInPropertyPlantAndEquipment"]
        self.acquisitions_net = entry["acquisitionsNet"]
        self.purchases_of_investments = entry["purchasesOfInvestments"]
        self.sales_maturities_of_investments = entry["salesMaturitiesOfInvestments"]
        self.other_investing_activites = entry["otherInvestingActivites"]
        self.net_cash_used_for_investing_activites = entry["netCashUsedForInvestingActivites"]
        self.debt_repayment = entry["debtRepayment"]
        self.common_stock_issued = entry["commonStockIssued"]
        self.common_stock_repurchased = entry["commonStockRepurchased"]
        self.dividends_paid = entry["dividendsPaid"]
        self.other_financing_activites = entry["otherFinancingActivites"]
        self.net_cash_used_provided_by_financing_activities = entry["netCashUsedProvidedByFinancingActivities"]
        self.effect_of_forex_changes_on_cash = entry["effectOfForexChangesOnCash"]
        self.net_change_in_cash = entry["netChangeInCash"]
        self.cash_at_end_of_period = entry["cashAtEndOfPeriod"]
        self.cash_at_beginning_of_period = entry["cashAtBeginningOfPeriod"]
        self.operating_cash_flow = entry["operatingCashFlow"]
        self.capital_expenditure = entry["capitalExpenditure"]
        self.free_cash_flow = entry["freeCashFlow"]
        self.link = entry["link"]
        self.final_link = entry["finalLink"]
