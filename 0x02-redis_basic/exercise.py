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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for
    a particular function.
    """
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input = str(args)
        key_prefix = method.__qualname__
        inputs_key = f"{key_prefix}:inputs"
        outputs_key = f"{key_prefix}:outputs"

        # Store the input parameters in Redis
        self._redis.rpush(inputs_key, input)

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(outputs_key, output)

        return output

    return wrapped


def replay(fn: Callable):
    """
    Display the history of calls of a particular function.
    """
    key_prefix = fn.__qualname__
    inputs_key = f"{key_prefix}:inputs"
    outputs_key = f"{key_prefix}:outputs"

    inputs = fn._redis.lrange(inputs_key, 0, -1)
    outputs = fn._redis.lrange(outputs_key, 0, -1)

    print(f"{key_prefix} was called {len(inputs)} times:")
    for input_str, output in zip(inputs, outputs):
        input_args = eval(input_str)
        input_str = ", ".join(map(repr, input_args))
        print(f"{key_prefix}(*({input_str},)) -> {output}")


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

    @count_calls
    @call_history
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
