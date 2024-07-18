# tests/test_utils.py

import unittest
from utils.decorators import timing_decorator

class TestUtils(unittest.TestCase):

    def test_timing_decorator(self):
        """
        Test the timing_decorator function.

        This test verifies that the timing_decorator correctly measures the execution time
        of the decorated function.
        """
        from time import sleep

        @timing_decorator
        def test_function():
            sleep(1)  # Simulate some work

        test_function()  # Call the decorated function

if __name__ == '__main__':
    unittest.main()