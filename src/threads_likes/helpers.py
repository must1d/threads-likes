import time
from typing import Callable


def retry(max_retries: int = 3, wait_seconds: float = 1.0) -> Callable:
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except:
                    retries += 1
                    if retries < max_retries:
                        time.sleep(wait_seconds)
                    else:
                        raise

        return wrapper

    return decorator
