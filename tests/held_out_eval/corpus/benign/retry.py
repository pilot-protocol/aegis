"""Exponential-backoff retry decorator for flaky network calls."""
import functools
import random
import time


def retry(attempts=3, base_delay=0.5, max_delay=8.0, exceptions=(Exception,)):
    """Retry the wrapped function with jittered exponential backoff."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == attempts:
                        raise
                    sleep_for = min(max_delay, delay) * (1 + random.random())
                    time.sleep(sleep_for)
                    delay *= 2
        return wrapper
    return decorator


@retry(attempts=5, exceptions=(TimeoutError,))
def fetch_remote(client, url):
    return client.get(url).json()
