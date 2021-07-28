from enum import Enum


class Status(Enum):
    SUCCESSFUL = "Successful"
    FAILED_INSUFFICIENT_FUNDS = "Failed - Insufficient Funds"
    FAILED_SYMBOL_NOT_FOUND = "Failed - Symbol not found"

class Transaction:
    def __init__(self, symbol: str, nb_shares: float, theoretical_price: float, simulated_price: float, timestamp, status: Status, transaction_fees: int)
        """
        Args:
            symbol (str): symbol for the stock (i.e. AAPL)
            nb_shares (float): Number of shares
            theoretical_price (float): Theoretical price of the shares
            simulated_price (float): Simulated price (with slippage) of the shares
            timestamp: Time of the transaction
            status : Status of the transaction
            transaction_fees: Fees of the transaction
        """
        self.symbol = symbol
        self.nb_shares = nb_shares
        self.theoretical_price = theoretical_price
        self.simulated_price = simulated_price
        self.timestamp = timestamp
        self.status = status
        self.transaction_fees = transaction_fees
