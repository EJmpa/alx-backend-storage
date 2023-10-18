#!/usr/bin/env python3
"""
Cache module
"""
import uuid
import redis
from typing import Callable, Union, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    Uses the qualified name of the method as the Redis key.
    """
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """wrapper for decorated function"""
        key = method.__qualname__
        count = self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapped


class Cache:
    """
    Cache class for storing data in Redis
    """

    def __init__(self):
        """
        Initializes the Cache with a Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data (Union[str, bytes, int, float]): Data to store.

        Returns:
            str: The random key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> \
            Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key. Optionally, apply a
        conversion function.

        Args:
            key (str): The key to retrieve data from.
            fn (Callable, optional): A callable function to convert the data.
            Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted by fn.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key to retrieve data from.

        Returns:
            str: The retrieved string value.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key to retrieve data from.

        Returns:
            int: The retrieved integer value.
        """
        return self.get(key, fn=int)
