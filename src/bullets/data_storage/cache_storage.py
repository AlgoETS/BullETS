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


def store_data_in_cache(endpoint: CacheEndpoint, symbol: str, section: str, data: str):
    file = os.path.join(CACHE, endpoint.value, symbol, section, "data.json")
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.isfile(file):
        pass
        # TODO: Merge new data with already cached data
    else:
        with open(file, "w") as outputFile:
            outputFile.write(data)


def check_data_in_cache(endpoint: CacheEndpoint, symbol: str, section: str, value: str):
    file = os.path.join(CACHE, endpoint.value, symbol, section, "data.json")
    if os.path.isfile(file):
        with open(file, "r") as dataFile:
            data = json.load(dataFile)
        __find_value__(endpoint, data, value)
    else:
        return None


def __find_value__(endpoint: CacheEndpoint, data: str, value: str):
    if endpoint is CacheEndpoint.PRICE:
        cp.find_value(data, value)
    elif endpoint is CacheEndpoint.STATEMENT:
        cs.find_value(data, value)
    elif endpoint is CacheEndpoint.LIST:
        cs.find_value(data, value)
