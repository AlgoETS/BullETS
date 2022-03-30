from enum import Enum
from appdirs import *

from bullets.data_storage.endpoints.cache_price import CachePrice
from bullets.data_storage.endpoints.cache_statement import CacheStatement


class LocalCache(Enum):
    """
    This enum links the different cache endpoints with their respective CacheInterface class
    """
    PRICE = CachePrice
    STATEMENT = CacheStatement


APP_NAME = "BullETS"
APP_AUTHOR = "AlgoETS"
CACHE = user_cache_dir(APP_NAME, APP_AUTHOR)


def store_data_in_cache(endpoint: LocalCache, section: str, file_name: str, data: str):
    """
    Stores the new data in the cache
    If this endpoint/section/symbol is new, save data to a new file (symbol)
    If this endpoint/section/symbol already exists, merge the new data with the old data in the right file (symbol)
    Args:
        endpoint: Endpoint in which the data will be stored (folder)
        section: Section of the endpoint in which the data will be stored (folder)
        file_name: Name of the file where the data will be saved
        data: The data that needs to be stored
    """
    file = os.path.join(CACHE, endpoint.name, section, file_name + ".json")
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.isfile(file):
        endpoint.value.merge_data(section, data, file)
    else:
        endpoint.value.post_data(section, data, file)


def get_data_in_cache(endpoint: LocalCache, section: str, file_name: str, timestamp: str, value: str):
    """
    Gets a specific value in the cache
    Args:
         endpoint: Endpoint in which the data is stored (folder)
         section: Section of the endpoint in which the data is stored (folder)
         file_name: Name of the file where the data is stored
         timestamp: The date/datetime of the value you need
         value: Specific value of the stored object you want (ex : open, low, close, etc.)
    """
    file = os.path.join(CACHE, endpoint.name, section, file_name + ".json")
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.isfile(file):
        return endpoint.value.get_data(section, file, timestamp, value)
    else:
        return None
