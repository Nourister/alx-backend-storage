#!/usr/bin/env python3

import redis
from typing import Callable

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

def replay(func: Callable):
    method_name = func.__qualname__
    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")

