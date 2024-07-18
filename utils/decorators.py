# utils/decorators.py

import time

def timing_decorator(func):
    """
    A decorator function to measure the execution time of a function.

    Args:
    - func: The function to be decorated.

    Returns:
    - wrapper function: A wrapper function that measures and prints the execution time
      of the decorated function.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that measures execution time and calls the decorated function.

        Args:
        - *args: Positional arguments to be passed to the decorated function.
        - **kwargs: Keyword arguments to be passed to the decorated function.

        Returns:
        - result: The result returned by the decorated function.
        """
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the decorated function with its arguments
        end_time = time.time()  # Record the end time
        # Print the execution time
        print(f"Execution time for '{func.__name__}': {end_time - start_time} seconds")
        return result  # Return the result of the decorated function

    return wrapper  # Return the decorated wrapper function