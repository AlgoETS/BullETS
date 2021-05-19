#“Data provided by Financial Modeling Prep
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

    async def request(self, endpoint: str, modifier = "") -> str:
        """
        Performs a request on the requested endpoint at the base url.
        Args:
            endpoint (str): Request endpoint e.g (/api/v3/profile/AAPL)
            modifier (str): allows to filter the result e.g (from=2018-03-12&to=2019-03-12&)

        Returns:
            JSON string with the response content
        """
        if endpoint:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{baseURL}{endpoint}?{modifier}apikey={self.token}') as response:
                    if response.status == 200:
                        return await response.text()