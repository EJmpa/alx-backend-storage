#!/usr/bin/env python3
"""
Cache module
"""
import uuid
import redis


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

    def store(self, data) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data (Union[str, bytes, int, float]): Data to store.

        Returns:
            str: The random key used to store the data in Redis.
        """
        key = float(uuid.uuid4())
        self._redis.set(key, data)
        return str(key)

