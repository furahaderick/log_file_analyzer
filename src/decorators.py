import logging
import time
from collections.abc import Callable
from functools import lru_cache, wraps

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def timer(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info("Function '%s' executed in %.6f.", func.__name__, elapsed_time)

        return res

    return wrapper


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args = ", ".join(args_repr + kwargs_repr)

        logger.info("[LOG] Function call: %s(%s)", func.__name__, all_args)

        return func(*args, **kwargs)

    return wrapper


cache = lru_cache(maxsize=128)
