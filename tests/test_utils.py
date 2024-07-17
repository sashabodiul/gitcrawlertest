# tests/test_utils.py

import unittest
from utils.decorators import timing_decorator

class TestUtils(unittest.TestCase):

    def test_timing_decorator(self):
        from time import sleep

        @timing_decorator
        def test_function():
            sleep(1)

        test_function()

if __name__ == '__main__':
    unittest.main()