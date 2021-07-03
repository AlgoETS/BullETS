import aiohttp
from bullets.data_source.data_source_interface import DataSourceInterface


class FmpDataSource(DataSourceInterface):
    BASE_URL = 'https://financialmodelingprep.com'

    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def get_price(self, symbol: str):
        """
        Gets the information of the stock at the current timestamp in the backtest
        Args:
            symbol: Symbol of the stock
        Returns: The tick information of the stock at the given timestamp
        """
        pass
        # TODO Get price from FMP at the current time

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
                async with session.get(f'{self.BASE_URL}{endpoint}?apikey={self.token}') as response:
                    if response.status == 200:
                        return await response.text()
