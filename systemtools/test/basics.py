# coding: utf-8
# pew in systemtools-venv python ./test/basics.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from systemtools import basics
from systemtools.basics import *

# The level allow the unit test execution to choose only the top level test
min = 0
max = 0
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(basics)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            pass

if min <= 2 <= max:
    class Test2(unittest.TestCase):
        def test1(self):
            d1 = [1, 2, 3]
            d2 = [2, 3, 4]
            d3 = [10, 11, 12]
            d4 = [1, 10]

            self.assertTrue(intersection([d1, d2]) == [2, 3])
            self.assertTrue(intersection([d1, d4]) == [1])
            self.assertTrue(intersection([d1, d3]) == [])
            self.assertTrue(intersection([d1, None]) == [])
            self.assertTrue(intersection([None, None]) == [])
            self.assertTrue(intersection(None) == [])
            self.assertTrue(intersection([None]) == [])
            self.assertTrue(intersection([d1, d2, d3, d4]) == [])
            self.assertTrue(intersection([d1, d2, d4]) == [])
            self.assertTrue(intersection([d1 + d2, d4]) == [1])

        def test2(self):
            d1 = ["aa", "bb"]
            d2 = "aa bb cc"
            d3 = ["cc", "ddd"]
            d4 = "aa dd cc"

            self.assertTrue(sorted(intersection([d1, d2])) == sorted(["bb", "aa"]))
            self.assertTrue(intersection([d3, d4]) == ["cc"])
            self.assertTrue(intersection([d1, d3, d2]) == [])
            self.assertTrue(intersection([d1, d2, d4]) == ["aa"])

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")