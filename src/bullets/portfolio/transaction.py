from enum import Enum


class Status(Enum):
    SUCCESSFUL = "Successful"
    FAILED_INSUFFICIENT_FUNDS = "Failed - Insufficient Funds"
    FAILED_SYMBOL_NOT_FOUND = "Failed - Symbol not found"

class Transaction:
    def __init__(self, symbol: str, nb_shares: float, price: float, timestamp, status: Status):
        """
        Args:
            symbol (str): symbol for the stock (i.e. AAPL)
            nb_shares (float): Number of shares
            price (float): Price of the shares
            timestamp: Time of the transaction
            status : Status of the transaction
        """
        self.symbol = symbol
        self.nb_shares = nb_shares
        self.price = price
        self.timestamp = timestamp
        self.status = status
