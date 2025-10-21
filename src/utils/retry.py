import time
import functools
from typing import Callable, Optional
from src.utils.logger import setup_logger

logger = setup_logger("retry")


def retry(max_attempts: int, backoff_seconds: float) -> Callable:
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_exc: Optional[BaseException] = None
            while attempt < max_attempts:
                attempt += 1
                try:
                    logger.info("Attempt %d/%d for %s", attempt, max_attempts, func.__name__)
                    return func(*args, **kwargs)
                except BaseException as exc:
                    last_exc = exc
                    logger.warning("Attempt %d failed for %s: %s", attempt, func.__name__, repr(exc))
                    if attempt >= max_attempts:
                        break
                    time.sleep(backoff_seconds)
            assert last_exc is not None
            raise last_exc
        return wrapper
    return decorator


