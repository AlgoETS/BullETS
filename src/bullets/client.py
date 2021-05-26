# Data provided by Financial Modeling Prep
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

    async def request(self, url: str) -> str:
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
