"""Test-it Mini Project
by Alex JPS
2023-01-17
CS 211
"""

import unittest
from buggy import *

class TestMaxRun(unittest.TestCase):

    def test_long_longer(self):
        """BUG: Not checking last run's length against max
        Test includes a short, long, and longer run."""
        self.assertEqual(max_run([1, 2, 2, 3, 3, 3]), [3, 3, 3])

    def test_empty_list(self):
        """BUG: Can't handle empty list, hardcoded reference to index 0
        Test includes empty list"""
        self.assertEqual(max_run([]), [])

    def test_max_run_example(self):
        """BUG: Failed example test case
        Test includes max run of 3 items between runs of 2 items"""
        self.assertEqual(max_run([1, 2, 2, 2, 3]), [2, 2, 2])


if __name__ == "__main__":
    unittest.main()