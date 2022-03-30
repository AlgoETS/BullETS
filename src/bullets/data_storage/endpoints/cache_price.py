import json
from datetime import datetime

from bullets.data_source.data_source_interface import Resolution
from bullets.data_source.recorded_data import PricePoint
from bullets.data_storage.endpoints.cache_interface import CacheInterface


class CachePrice(CacheInterface):
    @staticmethod
    def get_data(section: str, file: str, timestamp: str, value: str):
        with open(file, "r") as data_file:
            data = json.load(data_file)

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

    @staticmethod
    def post_data(section: str, data: str, file: bytes):
        with open(file, "w") as output_file:
            output_file.write(data)

    @staticmethod
    def merge_data(section: str, new_data: str, file: bytes):
        with open(file, "r") as cache_file:
            old_data = json.load(cache_file)

        new_data_json = json.loads(new_data)

        if section == Resolution.DAILY.name:
            old_data_prices = old_data["historical"]
            new_data_prices = new_data_json["historical"]
        else:
            old_data_prices = old_data
            new_data_prices = new_data_json

        for entry in new_data_prices:
            if entry not in old_data_prices:
                old_data_prices.append(entry)

        if section == Resolution.DAILY.name:
            old_data["historical"] = old_data_prices
        else:
            old_data = old_data_prices

        with open(file, "w") as cache_file:
            json.dump(old_data, cache_file, indent=1)


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
