# utils/decorators.py

import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for '{func.__name__}': {end_time - start_time} seconds")
        return result
    return wrapper