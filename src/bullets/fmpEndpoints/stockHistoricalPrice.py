from bullets.client import *
import json

#APIkey = '090bebac8a76a19401c9bb5561482a2c'

class StockHistoricalPrice:
    def __init__(self, APIKey : str):
        self.Client = Client(APIKey)
        self.Quote = ""

    def get_quote(self, resolution: str, ticker : str):
        self.Quote = Client.request(f'/api/v3/historical-chart/{resolution}/{ticker}')

    #def get_attr(self, attribut):