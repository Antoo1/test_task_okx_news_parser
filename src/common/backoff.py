import asyncio
from functools import wraps


def backoff(retry_count: int, exceptions: tuple[type[Exception], ...], timeout: float = 1):
    def wrapper(f):
        @wraps(f)
        async def _wrapped(*args, **kwargs):
            for attempt in range(retry_count):
                try:
                    return await f(*args, **kwargs)
                except exceptions:
                    if attempt < retry_count - 1:
                        await asyncio.sleep(timeout)
                        continue
                    raise
            raise NotImplemented

        return _wrapped
    return wrapper
