class Holding:
    def __init__(self, symbol: str):
        """
        Initializes the required variables for the Client

        Args:
            token (str): API key from FinancialModelPrep
        """
        self.symbol = symbol
        self.nb_shares = 0
        self.avg_price = 0

    def add_shares(self, nb_shares: float, price: float):
        """
        Args:
            nb_shares: Number of new shares
            price: Price of the new shares

        Raises:
        ZeroDivisionError: No more shares will be left in the holding.
        """
        self.avg_price = (self.avg_price * self.nb_shares + price * nb_shares)/(self.nb_shares + nb_shares)
        self.nb_shares = self.nb_shares + nb_shares
