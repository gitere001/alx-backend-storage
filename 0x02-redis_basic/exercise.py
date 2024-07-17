#!/usr/bin/env python3
"""contains the cache class"""
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable, Any


def count_calls(method: Callable) -> Callable:
    """keeps tally of the number of times methods are called"""
    @wraps(method)
    def invoker(self, *args, **kwargs):
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


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

    @call_history
    @count_calls
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

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float, None]:
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
