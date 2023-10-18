#!/usr/bin/env python3
"""
Web module for fetching and caching web content.
"""
import requests
import redis
from functools import wraps
from typing import Callable

# Create a Redis client
redis_client = redis.Redis()


def cache_result(fn: Callable) -> Callable:
    """
    Decorator to cache the result of a function.
    """
    @wraps(fn)
    def wrapped(url, *args, **kwargs):
        cache_key = f'cache:{url}'
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')

        result = fn(url, *args, **kwargs)
        redis_client.setex(cache_key, 10, result)
        return result

    return wrapped


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches the result with a
    10-second expiration.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The HTML content of the URL.
    """
    url_key = f'count:{url}'
    redis_client.incr(url_key)

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch content from {url}"


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    content = get_page(url)
    print(f"Content from {url}:\n{content}")

    access_count = redis_client.get(f'count:{url}')
    print(f"URL accessed {int(access_count)} times.")
