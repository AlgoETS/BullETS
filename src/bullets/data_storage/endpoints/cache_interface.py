from abc import abstractmethod


class CacheInterface:
    @staticmethod
    @abstractmethod
    def get_data(section: str, file: str, timestamp: str, value: str):
        """
        Gets a specific value in the cache
        Args:
            section: Section of the endpoint in which the data is stored (folder)
            file: Name of the file where the data is stored
            timestamp: The date/datetime of the value you need
            value: Specific value of the stored object you want (ex : open, low, close, etc.)
        """
        pass

    @staticmethod
    @abstractmethod
    def post_data(section: str, data: str, file: bytes):
        """
        Adds a new file in the cache
        Args:
            section: Section of the endpoint in which the data will be stored (folder)
            data: Data to store
            file: Name of the file where the data will be stored
        """
        pass

    @staticmethod
    @abstractmethod
    def merge_data(section: str, new_data: str, file: bytes):
        """
        Merges the new content to the existing content in the cache
        Args:
            section: Section of the endpoint in which the data will be merged (folder)
            new_data: New data to store
            file: Name of the file where the data is currently stored
        """
        pass
