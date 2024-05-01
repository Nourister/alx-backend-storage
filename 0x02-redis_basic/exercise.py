#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable
import functools

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
        self._call_counts = {}

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)

def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._call_counts[key] = self._call_counts.get(key, 0) + 1
        return method(self, *args, **kwargs)
    return wrapper
