# coding: utf-8

import subprocess
import time
import psutil
import inspect
import os
import glob
import sys
import re
import random
import string
import collections
import socket
from random import randint
from operator import itemgetter
import sh
import multiprocessing
import time
import signal
import getpass

from systemtools.basics import *
from psutil import virtual_memory



def getUsedPorts(logger=None):
    try:
        ports = []
        result = sh.netstat("-plntu")
        if result is not None and len(result) > 0:
            for line in result.splitlines():
                try:
                    line = line.split()
                    line = line[3].split(":")
                    port = line[-1]
                    port = int(port)
                    ports.append(port)
                except Exception as e:
                    if logger is not None:
                        logger.error(str(e))
        return ports
    except Exception as e:
        if logger is not None:
            logger.error(str(e))
        return []

def getUser():
    return getpass.getuser()

def callTimeoutHandler(signum, frame):
    raise Exception("Function call timeout.")
def setFunctionTimeout(*args, **kwargs):
    setCallTimeout(*args, **kwargs)
def setCallTimeout(timeout):
    signal.signal(signal.SIGALRM, callTimeoutHandler)
    signal.alarm(math.ceil(timeout))
def resetFunctionTimeout(*args, **kwargs):
    resetCallTimeout(*args, **kwargs)
def resetCallTimeout():
    setCallTimeout(0)

def ramAmount(*args, **kwargs):
    return getRAMTotal(*args, **kwargs)
def getRAMTotal():
    """
        Return a value in Go
    """
    mem = virtual_memory()
    return int(mem.total / pow(1024, 3))

def getProcCount(*args, **kwargs):
    return cpuCount(*args, **kwargs)
def cpuCount():
    return multiprocessing.cpu_count()


def disableWifi():
    sh.nmcli("radio", "wifi", "off")
    print("WiFi disabled!")
def enableWifi():
    sh.nmcli("radio", "wifi", "on")
    time.sleep(5)
    print("WiFi enabled!")

def isHostname(hostname):
    return getHostname().startswith(hostname)

def getHostname():
    return socket.gethostname()


# Deprecated (use sh lib instead):
def sleep(seconds):
    time.sleep(seconds)

# Deprecated (use sh lib instead):
def bash(text):
    """
        Deprecated: use sh lib instead
        But it doesn't work on eclipse, use instead a python command line
    """
    text = text.split(" ")
    return subprocess.call(text)

# Deprecated (use sh lib instead):
def bash2(text):
    """
        Deprecated: use sh lib instead
        But it doesn't work on eclipse, use instead a python command line
    """
    os.system(text)

# Deprecated (use sh lib instead):
def bash3(text):
    """
        Deprecated: use sh lib instead
        But it doesn't work on eclipse, use instead a python command line
    """
#     text = ['/bin/bash', '-c'] + text.split(" ")
    text = text.split(" ")
    return subprocess.check_output(text)

# Déprecated (use sh lib instead):
def bash4(text):
    """
        Deprecated: use sh lib instead
        But it doesn't work on eclipse, use instead a python command line
    """
#     text = ['/bin/bash', '-c'] + text.split(" ")
    text = text.split(" ")
    pipe = subprocess.Popen(text, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable='/bin/bash')
    stdout, stderr = pipe.communicate()
    return stdout

def enum(enumName, *listValueNames):
    """
    http://sametmax.com/faire-des-enums-en-python/
    >>> FeuCirculation.TOUT_ETEINT
    4
    >>> FeuCirculation.dictReverse[FeuCirculation.TOUT_ETEINT]
    'TOUT_ETEINT'
    """
    # Une suite d'entiers, on en crée autant
    # qu'il y a de valeurs dans l'enum.
    listValueNumbers = list(range(len(listValueNames)))
    # création du dictionaire des attributs.
    # Remplissage initial avec les correspondances : valeur d'enum -> entier
    dictAttrib = dict( list(zip(listValueNames, listValueNumbers)) )
    # création du dictionnaire inverse. entier -> valeur d'enum
    dictReverse = dict( list(zip(listValueNumbers, listValueNames)) )
    # ajout du dictionnaire inverse dans les attributs
    dictAttrib["dictReverse"] = dictReverse
    # création et renvoyage du type
    mainType = type(enumName, (), dictAttrib)
    return mainType


def stout():
    """
    Return True if we are on stout
    """
    return (psutil.cpu_count(logical=True) > 40) and ((psutil.virtual_memory().total / (1*(10**9))) > 40);

def getMemoryUsage(d):
    return asizeof(d)

def getMemoryPercent():
    return psutil.virtual_memory().percent

def printMemoryPercent():
    print("Memory usage: " + str(getMemoryPercent()) + "%")


def randomSleep(min=0.1, max=None):
    if max is None:
        max = min + 0.2 * min
    sleepDuration = getRandomFloat(min, max, decimalMax=8)
    time.sleep(sleepDuration)
    return sleepDuration


# Deprecated : use argparse instead
def argvOptionsToDict(argv=None):
    """
        This function convert a command in dict key values according to command options.
        If the function return None, it means the argv doesn't have a good format.

        :example:
        >>> argvOptionsToDict(argv=["thecommand", "-r", "r", "-a", "a"])
        {'a': 'a', 'r': 'r', 'command': 'thecommand'}
        >>> argvOptionsToDict(argv=["thecommand", "r", "r"]) is None
        True
        >>> argvOptionsToDict(argv=["thecommand"])
        {'command': 'thecommand'}
        >>> argvOptionsToDict(argv=["thecommand", "r"]) is None
        True
        >>> argvOptionsToDict(argv=["thecommand", "--abcd", "/abcd/e"])
        {'abcd': '/abcd/e', 'command': 'thecommand'}
    """
    if argv is None:
        argv = sys.argv
    argvDict = dict()
    if argv is None or len(argv) == 0 or len(argv) % 2 == 0:
        return None
    argvDict["command"] = argv[0]
    for i in range(1, len(argv), 2):
        current = argv[i]
        if len(current) == 2:
            if not current.startswith('-'):
                return None
            argvDict[str(current[1])] = argv[i + 1]
        elif len(current) >= 3:
            if not current.startswith('--'):
                return None
            argvDict[str(current[2:len(current)])] = argv[i + 1]
        else:
            return None
    return argvDict

# def argvOptionsToDict(argv=None):
#     """
#         This function convert a command in dict key values according to command options.
#         If the function return None, it means the argv doesn't have a good format.
#
#         :example:
#         >>> argvOptionsToDict(argv=["thecommand", "-r", "r", "-a", "a"])
#         {'a': 'a', 'r': 'r', '_command': 'thecommand'}
#         >>> argvOptionsToDict(argv=["thecommand"])
#         {'_command': 'thecommand'}
#         >>> argvOptionsToDict(argv=["thecommand", "r"]) is None
#         {'abcd': '/abcd/e', '_command': 'thecommand'}
#         >>> argvOptionsToDict(argv=["thecommand", "--abcd", "/abcd/e"])
#         {'abcd': '/abcd/e', '_command': 'thecommand'}
#         >>> argvOptionsToDict(argv=["thecommand", "abcd.md", "-r", "rrr", "afile.txt"])
#         {'_others': ["abcd.md", "afile.txt"], '_command': 'thecommand'}
#     """
#     if argv is None:
#         argv = sys.argv
#     argvDict = dict()
#     if argv is None or len(argv) == 0 or len(argv) % 2 == 0:
#         return None
#     argvDict["_command"] = argv[0]
#     for i in range(1, len(argv), 2):
#         current = argv[i]
#         if len(current) == 2:
#             if not current.startswith('-'):
#                 return None
#             argvDict[str(current[1])] = argv[i + 1]
#         elif len(current) >= 3:
#             if not current.startswith('--'):
#                 return None
#             argvDict[str(current[2:len(current)])] = argv[i + 1]
#         else:
#             return None
#     return argvDict

    # Get all index where there is "-". Jump after a "-":
#     optionIndexes = []
#     jumpNext = False
#     currentIndex = 1
#     while currentIndex < len(argv):
#         currentArg = argv[currentIndex]
#         if jumpNext:
#             jumpNext = False
#             currentIndex += 1
#         else:
#             if currentArg.startswith("-") and currentIndex < len(argv) - 1:
#                 optionIndexes.append(currentIndex)
#                 currentIndex += 2
#             else:
#                 currentIndex += 1
#
#     print optionIndexes



def test1():
    # This will give you [568, 905, 1114, 882, 1120, 899, 1074, 859, 1126, 900, 553] because 0 is a result of getRandomFloat() from 0.0 to 0.5, 10 is the result of 9.5 to 10.0
    count = [0] * 11
    for i in range(10000):
        current = int(round(getRandomFloat() * 10.0))
        count[current] += 1
    print(count)
    # So the solution is current = randint(0, 10) or:
    count = [0] * 11
    for i in range(10000):
        current = int(round(getRandomFloat() * 11.0 - 0.5))
        count[current] += 1
    print(count)



if __name__ == "__main__":
    print(getRAMTotal())

# TODO
"""def copyDirectory(src, dst, symlinks=False, ignore=None):
    newFolder = re.search("/(\w+)/?$", src).group(1)
    if dst[-1] != "/":
        dst += "/"
    newFolderPath = dst + newFolder + "/"
    shutil.rmtree(newFolderPath)
    mkdirIfNotExists(newFolderPath)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)"""


