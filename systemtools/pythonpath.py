# coding: utf-8


import os
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

for current in user_paths:
    print(current)