class Transaction:
    def __init__(self, ticker: str, nb_shares: float, price: float, timestamp):
        """
        Args:
            ticker (str): Ticker for the stock (i.e. AAPL)
            nb_shares (float): Number of shares
            price (float): Price of the shares
            timestamp: Time of the transaction
        """
        self.ticker = ticker
        self.nb_shares = nb_shares
        self.price = price
        self.timestamp = timestamp
