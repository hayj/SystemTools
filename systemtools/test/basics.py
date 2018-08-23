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
mini = 0
maxi = 8
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(basics)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            pass

if mini <= 2 <= maxi:
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

if mini <= 3 <= maxi:
    class Test3(unittest.TestCase):
        def test1(self):
            l = list(range(100))
            result = chunks(l, 6)
            printLTS(result)
            self.assertTrue(len(result) == math.ceil(100/6))
            result = split(l, 6)
            printLTS(result)
            self.assertTrue(len(result) == 6)


            l = list(range(7))
            result = chunks(l, 6)
            printLTS(result)
            self.assertTrue(len(result) == 2)
            self.assertTrue(len(result[0]) == 6)
            self.assertTrue(len(result[1]) == 1)
            result = split(l, 6)
            printLTS(result)
            self.assertTrue(len(result) == 6)

            l = []
            result = chunks(l, 1)
            self.assertTrue(len(result) == 0)
            result = chunks(l, 2)
            self.assertTrue(len(result) == 0)
            result = split(l, 1)
            self.assertTrue(len(result) == 1)
            result = split(l, 2)
            self.assertTrue(len(result) == 2)

            l = None
            self.assertTrue(split(l, 1) == [])
            self.assertTrue(chunks(l, 1) == [])

            l = [1]
            result = chunks(l, 1)
            self.assertTrue(len(result) == 1)
            self.assertTrue(len(result[0]) == 1)
            result = chunks(l, 2)
            self.assertTrue(len(result) == 1)
            self.assertTrue(result == [[1]])
            result = split(l, 1)
            self.assertTrue(len(result) == 1)
            self.assertTrue(result == [[1]])
            result = split(l, 2)
            self.assertTrue(len(result) == 2)
            self.assertTrue(result == [[1], []])

            l = list(range(10))
            result = chunks(l, 12)
            printLTS(result)
            self.assertTrue(len(result) == 1)
            result = split(l, 12)
            self.assertTrue(len(result) == 12)


            l = [1]
            result = split(l, 1)
            self.assertTrue(len(result) == 1)
            l = [1]
            result = split(l, 6)
            self.assertTrue(len(result) == 6)

if mini <= 4 <= maxi:
    class Test4(unittest.TestCase):
        def test1(self):
            o1 = \
            {
                "summary_detail": \
                {
                    "language": None,
                    "test": 1,
                },
                "link": "http://...",
            }

            self.assertTrue(
                getDictSubElement(o1, ["summary_detail", "language"]) == None)
            self.assertTrue(
                getDictSubElement(o1, ["summary_detail", "test"]) == 1)
            self.assertTrue(
                getDictSubElement(o1, ["summary_detail", "a"]) == None)
            self.assertTrue(
                getDictSubElement(o1, ["summary", "test"]) == None)
            self.assertTrue(
                getDictSubElement(o1, ["link", "test"]) == None)
            self.assertTrue(
                getDictSubElement(o1, ["link"]) == "http://...")

            o1 = \
            {
                "summary_detail": \
                {
                    "language": {"test": 2},
                    "test": 1,
                },
                "link": "http://...",
            }
            self.assertTrue(
                getDictSubElement(o1, ["summary_detail", "language"]) == {"test": 2})
            self.assertTrue(
                getDictSubElement(o1, ["summary_detail", "language", "test"]) == 2)


if mini <= 5 <= maxi:
    class Test5(unittest.TestCase):
        def test1(self):
            t = "aa \n       uu.\roo\trr "
            reducedT = reduceBlank(t, keepNewLines=False)
            knlReducedT = reduceBlank(t, keepNewLines=True)
            self.assertTrue(reducedT == "aa uu. oo rr")
            self.assertTrue(knlReducedT == "aa\nuu.\noo rr")

            t = "\n\n\naa.bb      oo\n"
            reducedT = reduceBlank(t, keepNewLines=False)
            knlReducedT = reduceBlank(t, keepNewLines=True)
            self.assertTrue(reducedT == "aa.bb oo")
            self.assertTrue(knlReducedT == "aa.bb oo")


if mini <= 6 <= maxi:
    class Test6(unittest.TestCase):
        def test1(self):
            l = list(range(10))
            l = splitMaxSized(l, 5)
            self.assertTrue(len(l) == 2)
            self.assertTrue(len(l[0]) == 5)
            self.assertTrue(len(l[1]) == 5)

            l = list(range(9))
            l = splitMaxSized(l, 5)
            self.assertTrue(len(l) == 2)
            self.assertTrue(len(l[0]) == 5)
            self.assertTrue(len(l[1]) == 4)

            l = list(range(11))
            l = splitMaxSized(l, 5)
            self.assertTrue(len(l) == 3)
            self.assertTrue(len(l[0]) == 4)
            self.assertTrue(len(l[1]) == 4)
            self.assertTrue(len(l[2]) == 3)

            l = list(range(1))
            l = splitMaxSized(l, 5)
            self.assertTrue(len(l) == 1)
            self.assertTrue(len(l[0]) == 1)

            l = list(range(11))
            l = splitMaxSized(l, 0)
            self.assertTrue(len(l) == 1)
            self.assertTrue(len(l[0]) == 11)

            l = list(range(11))
            l = splitMaxSized(l, 1)
            self.assertTrue(len(l) == 11)
            self.assertTrue(len(l[0]) == 1)
            self.assertTrue(len(l[1]) == 1)
            self.assertTrue(len(l[2]) == 1)


if __name__ == '__main__':
    unittest.main() # Orb execute as Python unit-test in eclipse


print("Unit tests done.\n==============")