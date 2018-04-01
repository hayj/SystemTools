# coding: utf-8
# pew in systemtools-venv python ./test/filetest.py

import os
import sys
from pip.utils.deprecation import RemovedInPip10Warning
sys.path.append('../')

import unittest
import doctest
from systemtools.basics import *
from systemtools import file
from systemtools.file import *

# The level allow the unit test execution to choose only the top level test
min = 0
max = 10
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(file)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            print("Please check by hand:")
            input()
            file1 = "/home/hayj/Data/Misc/crawling/shorteners.txt"
            file2 = "/home/hayj/Data/Misc/crawling/proxies/proxies-failed.txt"
            file3 = "/home/hayj/Data/Misc/crawling/proxies/proxies-renew.txt"

            printLTS(fileToStrList(file1))
            printLTS(fileToStrList(file1, removeDuplicates=True))
            input()
            printLTS(fileToStrList(file2))
            printLTS(fileToStrList(file2, commentStart="==>"))
            input()
            printLTS(fileToStrList(file3))
            printLTS(fileToStrList(file3, skipBlank=False))

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")