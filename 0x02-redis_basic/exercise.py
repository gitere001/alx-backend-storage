#!/usr/bin/env python3
"""contains the cache class"""
import redis
import uuid
from typing import Union


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
