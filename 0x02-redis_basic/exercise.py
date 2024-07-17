#!/usr/bin/env python3
"""contains the cache class"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """
    The cache class provides an interface to store data in a cache.
    The cache is implemented using Redis.
    """

    def __init__(self) -> None:
        """
        Initialize a cache. The cache is empty at initialization.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in the cache with a unique key generated using
        uuid.

        :param data: The data to be stored in the cache
        :type data: str or bytes

        :return: The key used to store the data in the cache.
        :rtype: str
        """

        key = str(uuid.uuid4())

        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable]=None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the value associated with the given key from the Redis cache.

        Parameters:
            key (str): The key used to identify the value in the cache.
            fn (Optional[Callable]): An optional function to apply to the
            retrieved value before returning it. Defaults to None.

        Returns:
            The value associated with the given key, or None if the key does
            not exist in the cache.
            If a function is provided, the value is passed to the function
            before being returned.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the value associated with the given key from the Redis cache
        and decodes it as a UTF-8 string.

        Parameters:
            key (str): The key used to identify the value in the cache.

        Returns:
            str: The decoded value associated with the given key, or None if
            the key does not exist in the cache.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the value associated with the given key from the Redis cache
        and converts it to an integer.

        Parameters:
            key (str): The key used to identify the value in the cache.

        Returns:
            int: The integer value associated with the given key, or None if
            the key does not exist in the cache.

        """
        return self.get(key, int)
