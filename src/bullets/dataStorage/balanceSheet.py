

class Assets:
    __slots__ = ["tax", "intangible", "non_current_others", "non_current_total",
                 "current_others", "current_total", "others", "total"]

    def __init__(self, data: dict):
        """
        Initializes the required variable for the Expenses

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        self.tax = data["taxAssets"]
        self.intangible = data["intangibleAssets"]
        self.non_current_others = data["otherNonCurrentAssets"]
        self.non_current_total = data["totalNonCurrentAssets"]
        self.current_others = data["otherCurrentAssets"]
        self.current_total = data["totalCurrentAssets"]
        self.others = data["otherAssets"]
        self.total = data["totalAssets"]


class Liabilities:
    __slots__ = ["deferred_revenue", "non_current_deferred_revenue",
                 "non_current_deferred_tax", "non_current_others", "non_current_total",
                 "current_others", "current_total", "others", "total"]

    def __init__(self, data: dict):
        """
        Initializes the required variable for the Expenses

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        self.deferred_revenue = data["deferredRevenue"]
        self.non_current_deferred_revenue = data["deferredRevenueNonCurrent"]
        self.non_current_deferred_tax = data["deferredTaxLiabilitiesNonCurrent"]
        self.non_current_others = data["otherNonCurrentLiabilities"]
        self.non_current_total = data["totalNonCurrentLiabilities"]
        self.current_others = data["otherCurrentLiabilities"]
        self.current_total = data["totalCurrentLiabilities"]
        self.others = data["otherLiabilities"]
        self.total = data["totalLiabilities"]


class BalanceSheet:
    __slots__ = ["liquidity", "short_term_investments", "long_term_investments",
                 "short_term_debt", "long_term_debt", "net_receivables", "inventory",
                 "assets", "liabilities", "property_equipment", "goodwill",
                 "account_payables", "tax_payables", "common_stock",
                 "stock_holders_equity", "retained_earnings"]

    def __init__(self, data: dict):
        """
        Initializes the required variable for the IncomeStatement

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        self.liquidity = data["cashAndCashEquivalents"]
        self.short_term_investments = data["shortTermInvestments"]
        self.long_term_investments = data["longTermInvestments"]
        self.short_term_debt = data["shortTermDebt"]
        self.long_term_debt = data["longTermDebt"]
        self.net_receivables = data["netReceivables"]
        self.inventory = data["inventory"]
        self.assets = Assets(data)
        self.liabilities = Liabilities(data)
        self.property_equipment = data["propertyPlantEquipmentNet"]
        self.goodwill = data["goodwill"]
        self.account_payables = data["accountPayables"]
        self.tax_payables = data["taxPayables"]
        self.common_stock = data["commonStock"]
        self.stock_holders_equity = data["totalStockholdersEquity"]
        self.retained_earnings = data["retainedEarnings"]
