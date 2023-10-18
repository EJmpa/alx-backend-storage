#!/usr/bin/env python3
"""
Web module for fetching and caching web content.
"""
import requests
import redis
from functools import wraps

# Create a Redis client
redis_client = redis.Redis()


def cache_result(fn):
    """
    Decorator to cache the result of a function.
    """
    @wraps(fn)
    def wrapped(url, *args, **kwargs):
        # Check if the result is already cached
        cached_result = redis_client.get(f'cache:{url}')
        if cached_result:
            return cached_result.decode('utf-8')

        result = fn(url, *args, **kwargs)
        redis_client.setex(f'cache:{url}', 10, result)
        return result

    return wrapped


def track_access_count(fn):
    """
    Decorator to track the access count of a URL.
    """
    @wraps(fn)
    def wrapped(url, *args, **kwargs):
        url_key = f'count:{url}'
        redis_client.incr(url_key)
        return fn(url, *args, **kwargs)

    return wrapped


@track_access_count
@cache_result
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches the result with a
    10-second expiration.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch content from {url}"


if __name__ == "__main__":
    # Test the get_page function with a slow URL
    url = "http://slowwly.robertomurray.co.uk/delay\
    /5000/url/https://www.example.com"
    content = get_page(url)
    print(f"Content from {url}:\n{content}")

    access_count = redis_client.get(f'count:{url}')
    print(f"URL accessed {int(access_count)} times.")
