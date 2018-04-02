# coding: utf-8
# pew in systemtools-venv python ./test/number.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from systemtools import number
from systemtools.number import *

# The level allow the unit test execution to choose only the top level test
mini = 0
maxi = 5
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(number)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            pass



if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")