# coding: utf-8




import unittest
import doctest
from systemtools import duration
from systemtools.duration import *;
import time

# The level allow the unit test execution to choose only the top level test 
min = 0
max = 1
assert min <= max

print("\n==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(duration)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def testTicToc(self):
            tt = TicToc(maxDecimal=4);
            tt.tic();
            time.sleep(1);
            temp = tt.tic();
            self.assertTrue(temp > 0.9)
            time.sleep(1);
            tt.tic();
            time.sleep(1);
            tt.setMaxDecimal(2);
            tt.toc();
            time.sleep(1);
            tt.tic();
            time.sleep(1);
            end = tt.toc();
            self.assertTrue(end > 4.9)

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")




            
        

