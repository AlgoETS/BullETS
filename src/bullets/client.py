import aiohttp

__all__ = ["Client"]

baseURL = 'https://financialmodelingprep.com'


class Client:
    def __init__(self, token: str):
        """
        Initializes the required variables for the Client

        Args:
            token (str): API key from FinancialModelPrep
        """
        self.token = token

    async def request(self, endpoint: str) -> str:
        """
        Performs a request on the requested endpoint at the base url.
        Args:
            endpoint: Request endpoint e.g (/api/v3/profile/AAPL)

        Returns:
            JSON string with the response content
        """
        if endpoint:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{baseURL}{endpoint}?apikey={self.token}') as response:
                    if response.status == 200:
                        return await response.text()