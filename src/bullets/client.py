from bullets.dataStorage.stock import *
from bullets.resolution import *
from datetime import date
import aiohttp

__all__ = ["Client"]


class Client:
    def __init__(self, token: str):
        """
        Initializes the required variables for the Client

        Args:
            token (str): API key from FinancialModelPrep
        """
        self.token = token

    @staticmethod
    async def request(url: str) -> str:
        """
        Performs a request on the requested endpoint at the base url.
        Args:
            url (str): address with endpoint to retrieve data

        Returns:
            JSON string with the response content
        """
        if url:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()

    def load_historical_price(self, stock: Stock, start_date: date, end_date: date):
        """
        Performs a request on the requested endpoint at the base url.

        Args:
            stock (Stock): address with endpoint to retrieve data
            start_date (date): The earliest date to retrieve data
            end_date (date): The latest date to retrieve data

        """
        pass

    def load_company_profile(self, stock: Stock):
        """
        Performs a request on the requested endpoint at the base url.

        Args:
            stock (Stock): address with endpoint to retrieve data
        """
        pass

    def load_income_statement(self, stock: Stock, timespan=Timespan.Yearly):
        """
        Performs a request on the requested endpoint at the base url.

        Args:
            stock (Stock): address with endpoint to retrieve data
            timespan (str): period that the statement applies
                            (only quarterly and yearly are accepted values)
        """
        pass

    def load_balance_sheet(self, stock: Stock, timespan=Timespan.Yearly):
        """
        Performs a request on the requested endpoint at the base url.

        Args:
            stock (Stock): address with endpoint to retrieve data
            timespan (str): period that the statement applies
                            (only quarterly and yearly are accepted values)
        """
        pass

    def load_cash_flow(self, stock: Stock, timespan=Timespan.Yearly):
        """
        Performs a request on the requested endpoint at the base url.

        Args:
            stock (Stock): address with endpoint to retrieve data
            timespan (str): period that the statement applies
                            (only quarterly and yearly are accepted values)
        """
        pass
