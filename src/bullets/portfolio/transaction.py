class Transaction:
    STATUS_SUCCESSFUL = "Successful"
    STATUS_FAILED_INSUFFICIENT_FUNDS = "Failed - Insufficient Funds"
    STATUS_FAILED_SYMBOL_NOT_FOUND = "Failed - Symbol couldn't be found"

    def __init__(self, symbol: str, nb_shares: float, price: float, timestamp, status: str):
        """
        Args:
            symbol (str): symbol for the stock (i.e. AAPL)
            nb_shares (float): Number of shares
            price (float): Price of the shares
            timestamp: Time of the transaction
        """
        self.symbol = symbol
        self.nb_shares = nb_shares
        self.price = price
        self.timestamp = timestamp
        self.status = status
