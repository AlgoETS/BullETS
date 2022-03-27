import json
from datetime import datetime

from bullets.data_source.data_source_interface import Resolution
from bullets.data_source.recorded_data import PricePoint


def get_data(section: str, data: str, timestamp: str, value: str):
    if section == Resolution.DAILY.name:
        historical_prices = data["historical"]
    else:
        historical_prices = data
    for entry in historical_prices:
        price_point = PricePoint(entry)
        if section == Resolution.DAILY.name:
            stock_date = datetime.strptime(price_point.date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        else:
            stock_date = datetime.strptime(price_point.date, "%Y-%m-%d %H:%M:%S")
        if stock_date == timestamp:
            return _get_specific_stock_value(price_point, value)
    return None


def store_data(section: str, new_data: str, file: bytes):
    with open(file, "r") as cacheFile:
        old_data = json.load(cacheFile)
    # TODO: Merge new_data with old_data
    pass


def _get_specific_stock_value(price_point: PricePoint, value: str):
    if value is None or value == "close":
        return price_point.close
    elif value == "date":
        return price_point.date
    elif value == "open":
        return price_point.open
    elif value == "low":
        return price_point.low
    elif value == "high":
        return price_point.high
    elif value == "volume":
        return price_point.volume
