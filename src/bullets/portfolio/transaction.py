from datetime import datetime
from enum import Enum
from bullets import logger


class Status(Enum):
    SUCCESSFUL = "Successful"
    FAILED_INSUFFICIENT_FUNDS = "Failed - Insufficient Funds"
    FAILED_SYMBOL_NOT_FOUND = "Failed - Symbol not found"

    def __str__(self):
        if self == Status.SUCCESSFUL:
            return "SUCCESSFUL"
        elif self == Status.FAILED_INSUFFICIENT_FUNDS:
            return "FAILED_INSUFFICIENT_FUNDS"
        elif self == Status.FAILED_SYMBOL_NOT_FOUND:
            return "FAILED_SYMBOL_NOT_FOUND"


class Transaction:
    def __init__(self, symbol: str, nb_shares: float, theoretical_price: float, simulated_price: float,
                 timestamp: datetime, cash_balance: float, status: Status, transaction_fees: int, order_type: str,
                 total_balance_before_transaction: float):
        self.symbol = symbol
        self.nb_shares = nb_shares
        self.theoretical_price = theoretical_price
        self.simulated_price = simulated_price
        if simulated_price is None or nb_shares is None:
            self.total_price = None
        else:
            self.total_price = nb_shares * simulated_price
        self.timestamp = timestamp
        self.cash_balance = cash_balance
        self.status = status
        self.transaction_fees = transaction_fees
        self.order_type = order_type
        if self.status == Status.SUCCESSFUL:
            self.total_balance_after_transaction = total_balance_before_transaction - self.total_price

        else:
            self.total_balance_after_transaction = total_balance_before_transaction
        self._log()

    def _log(self):
        log = "(" + str(self.status.value) + ") " + self.order_type + ": "
        if self.timestamp is not None:
            log += str(self.timestamp) + " - "
        log += self.symbol + " - " + str(self.nb_shares) + " shares "
        if self.simulated_price is not None:
            log += "@ " + str(self.simulated_price) + "$"
        if self.status == Status.FAILED_INSUFFICIENT_FUNDS:
            log += " -  cash balance : " + str(self.cash_balance) + "$"
        logger.info(log)

    def to_dict(self):
        self_dict = {}
        self_dict['timestamp'] = self.timestamp.__str__()
        self_dict['symbol'] = self.symbol
        self_dict['nb_shares'] = self.nb_shares
        self_dict['theorical_price'] = self.theoretical_price
        self_dict['simulated_price'] = self.simulated_price
        self_dict['total_price'] = self.total_price
        self_dict['cash_balance'] = self.cash_balance
        self_dict['status'] = self.status.__str__()
        self_dict['transaction_fees'] = self.transaction_fees
        self_dict['order_type'] = self.order_type
        self_dict['total_balance_after'] = self.total_balance_after_transaction
        return self_dict
