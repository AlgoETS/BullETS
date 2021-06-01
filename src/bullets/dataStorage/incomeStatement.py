

class Expenses:
    __slots__ = ["research_development", "general_administration",
                 "selling_marketing", "operating", "interest",
                 "income_tax", "other"]

    def __init__(self, data: dict):
        """
        Initializes the required variable for the Expenses

        Args: datapoint of a ticker for a specific timeframe

        """
        self.research_development = data["researchAndDevelopmentExpenses"]
        self.general_administration = data["generalAndAdministrativeExpenses"]
        self.selling_marketing = data["sellingAndMarketingExpenses"]
        self.operating = data["operatingExpenses"]
        self.interest = data["interestExpense"]
        self.income_tax = data["incomeTaxExpense"]
        self.other = data["otherExpenses"]


class IncomeStatement:
    __slots__ = ["revenue", "cost_revenue", "gross_profit", "expenses",
                 "depreciation", "ebitda", "operating_income",
                 "income_before_tax", "net_income"]

    def __init__(self, data: dict):
        """
        Initializes the required variable for the IncomeStatement

        Args:
            data (dict): datapoint of a ticker for a specific timeframe
        """
        self.revenue = data["revenue"]
        self.cost_revenue = data["costOfRevenue"]
        self.gross_profit = data["grossProfit"]
        self.expenses = Expenses(data)
        self.depreciation = data["depreciationAndAmortization"]
        self.ebitda = data["ebitda"]
        self.operating_income = data["operatingIncome"]
        self.income_before_tax = data["incomeBeforeTax"]
        self.net_income = data["netIncome"]
