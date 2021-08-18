

class Holding:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.nb_shares = 0
        self.avg_price = 0
        self.current_price = 0

    def add_shares(self, nb_shares: float, price: float) -> float:
        """
        Add a certain amount of shares at a specific price to your holdings
        Args:
            nb_shares: Number of new shares
            price: Price of the new shares
        Returns: Number of shares owned
        """
        new_nb_shares = self.nb_shares + nb_shares
        if new_nb_shares == 0:
            self.avg_price = 0
            return 0
        self.avg_price = (self.avg_price * self.nb_shares + price * nb_shares)/new_nb_shares
        self.nb_shares = new_nb_shares
        return self.nb_shares
