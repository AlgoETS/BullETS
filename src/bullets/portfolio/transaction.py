from datetime import datetime
from enum import Enum
from bullets import logger


class Status(Enum):
    SUCCESSFUL = "Successful"
    FAILED_INSUFFICIENT_FUNDS = "Failed - Insufficient Funds"
    FAILED_SYMBOL_NOT_FOUND = "Failed - Symbol not found"


class Transaction:
    def __init__(self, symbol: str, nb_shares: float, theoretical_price: float, simulated_price: float,
                 timestamp: datetime, cash_balance: float, status: Status, transaction_fees: int, order_type: str):
        """
        Args:
            symbol (str): symbol for the stock (i.e. AAPL)
            nb_shares (float): Number of shares
            theoretical_price (float): Theoretical price of the shares
            simulated_price (float): Simulated price (with slippage) of the shares
            timestamp: Time of the transaction
            cash_balance: The portfolio's cash balance at the time of the transaction
            status : Status of the transaction
            transaction_fees: Fees of the transaction
        """
        self.symbol = symbol
        self.nb_shares = nb_shares
        self.theoretical_price = theoretical_price
        self.simulated_price = simulated_price
        self.timestamp = timestamp
        self.cash_balance = cash_balance
        self.status = status
        self.transaction_fees = transaction_fees
        self.order_type = order_type
        self.__log__()

    def __log__(self):
        log = "(" + str(self.status.value) + ") " + self.order_type + ": "
        if self.timestamp is not None:
            log += str(self.timestamp) + " - "
        log += self.symbol + " - " + str(self.nb_shares) + " shares "
        if self.simulated_price is not None:
            log += "@ " + str(self.simulated_price) + "$"
        if self.status == Status.FAILED_INSUFFICIENT_FUNDS:
            log += " -  cash balance : " + str(self.cash_balance) + "$"
        logger.info(log)
