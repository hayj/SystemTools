# coding: utf-8
# cd /home/hayj/Workspace/Python/Utils/SystemTools && python setup.py install && pew in systemtools-venv python ./systemtools/test/systemtest.py

import os
exec(compile(open(os.path.dirname(os.path.abspath(__file__)) + "/setpythonpath.py").read(), os.path.dirname(os.path.abspath(__file__)) + "/setpythonpath.py", 'exec'), {})


import unittest
import doctest
from systemtools import system
from systemtools.system import *
import sh
import glob

# The level allow the unit test execution to choose only the top level test 
min = 1
max = 1
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(system)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            
            argvOptionsToDict(argv=["thecommand", "abcd.md", "-r", "rrr", "afile.txt"])
            argvOptionsToDict(argv=["thecommand", "abcd.md", "-r"])

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")



