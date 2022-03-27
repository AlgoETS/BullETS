import json
from enum import Enum
from appdirs import *

from bullets.data_storage.endpoints import cache_price as cp
from bullets.data_storage.endpoints import cache_statement as cs
from bullets.data_storage.endpoints import cache_list as cl


class CacheEndpoint(Enum):
    PRICE = "PRICE"
    STATEMENT = "STATEMENT"
    LIST = "LIST"


APP_NAME = "BullETS"
APP_AUTHOR = "AlgoETS"
CACHE = user_cache_dir(APP_NAME, APP_AUTHOR)


def store_data_in_cache(endpoint: CacheEndpoint, section: str, symbol: str, data: str):
    file = os.path.join(CACHE, endpoint.value, section, symbol + ".json")
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.isfile(file):
        _store_data_in_endpoint(endpoint, section, data, file)
    else:
        with open(file, "w") as outputFile:
            outputFile.write(data)


def get_data_in_cache(endpoint: CacheEndpoint, section: str, symbol: str, timestamp: str, value: str):
    file = os.path.join(CACHE, endpoint.value, section, symbol + ".json")
    if os.path.isfile(file):
        with open(file, "r") as dataFile:
            data = json.load(dataFile)
        return _get_data_in_endpoint(endpoint, section, data, timestamp, value)
    else:
        return None


def _store_data_in_endpoint(endpoint: CacheEndpoint, section: str, new_data: str, file: bytes):
    if endpoint is CacheEndpoint.PRICE:
        return cp.store_data(section, new_data, file)
    elif endpoint is CacheEndpoint.STATEMENT:
        return cs.store_data(section, new_data, file)
    elif endpoint is CacheEndpoint.LIST:
        return cl.store_data(section, new_data, file)


def _get_data_in_endpoint(endpoint: CacheEndpoint, section: str, data: str, timestamp: str, value: str):
    if endpoint is CacheEndpoint.PRICE:
        return cp.get_data(section, data, timestamp, value)
    elif endpoint is CacheEndpoint.STATEMENT:
        return cs.get_data(data, value)
    elif endpoint is CacheEndpoint.LIST:
        return cl.get_data(data, value)

