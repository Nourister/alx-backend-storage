#!/usr/bin/env python3

import redis
import uuid
from typing import Callable
from functools import wraps

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def call_history(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = method.__qualname__ + ":inputs"
            output_key = method.__qualname__ + ":outputs"

            # Store input arguments
            self._redis.rpush(input_key, str(args))

            # Execute the wrapped function to retrieve the output
            output = method(self, *args, **kwargs)

            # Store the output
            self._redis.rpush(output_key, str(output))

            return output
        return wrapper

    @call_history
    def store(self, data):
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key):
        return self._redis.get(key)
