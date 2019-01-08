# coding: utf-8

import math
from collections import OrderedDict
import random
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
import csv
import json
from collections import OrderedDict
import hashlib
import unicodedata
import random
import re
import string
from systemtools.location import enhanceDir, getExecDir
from datetime import datetime
import parsedatetime
import arrow
from enum import Enum
from pytz import timezone
import pytz
from tzlocal import get_localzone
from dateutil import tz
from dateutil.tz import tzlocal
from systemtools.number import *
from tabulate import tabulate
import itertools



def intByteSize(n):
    if n == 0:
        return 1
    return int(math.log(n, 256)) + 1


# merge = \
# {
#     1: {2, 3, 4},
#     2: {1, 3, 4},
#     4: {1, 2, 3},
#     3: {1, 2, 4},
#     5: {6, 8},
#     6: {5, 8},
#     8: {6, 5},
# }

# print(recursiveFind(merge, [1, 6]))

# exit()


def mergeDuplicates(dups):
    def recursiveFind(merge, l, alreadyVisited=set()):
        all = set(l)
        for current in l:
            if current in merge and current not in alreadyVisited:
                alreadyVisited.add(current)
                all = all.union(recursiveFind(merge, merge[current], alreadyVisited))
        return all
    dups = list(itertools.chain(*dups))
    prevousLen = -1
    while prevousLen - len(dups) != 0:
        prevousLen = len(dups)
        merge = dict()
        for dup in dups:
            all = recursiveFind(merge, dup)
            for a in all:
                for b in all:
                    if a not in merge:
                        merge[a] = set()
                    merge[a].add(b)
        result = []
        for current in merge.values():
            if current not in result:
                result.append(current)
        dups = result
    return dups

def findDuplicates(texts, strip=True, useSets=True):
    """
        The returned structure looks like this:

        [
            {0, 1},
            {2},
            {3, 5},
            {4}
        ]
    """
    duplicates = dict() # {<text>: <duplicates ids set>}
    i = 0
    for text in texts:
        if strip:
            text = stripAll(text)
        if text not in duplicates:
            duplicates[text] = [i]
        else:
            duplicates[text].append(i)
        i += 1
    if useSets:
        duplicatesResult = []
        for text, currentDuplicates in duplicates.items():
            if len(currentDuplicates) > 1:
                duplicatesResult.append(set(currentDuplicates))
        return duplicatesResult
    else:
        result = []
        for current in duplicates.values():
            if len(current) > 1:
                result.append(current)
        return result


def strip(text):
    if text is None or not isinstance(text, str):
        return None
    else:
        return text.strip()

def trim(*args, **kwargs):
    return reduceBlank(*args, **kwargs)
def trimAll(*args, **kwargs):
    return reduceBlank(*args, **kwargs)
def stripAll(*args, **kwargs):
    return reduceBlank(*args, **kwargs)
def reduceBlank(text, keepNewLines=False):
    """
        Strip a string and reduce all blank space to a unique space. If you set keepNewLines as True, it will keep a unique '\n' at each blank space which contains a '\n' or a '\r'
    """
    if text is None:
        return None
    text = text.strip()
    if not keepNewLines:
        return re.sub(r'\s+', ' ', text)
    else:
        text = re.sub(r'\r', '\n', text)
        text = re.sub(r'\s*\n+\s*', '\n', text)
        text = re.sub(r'[ \t\f\v]+', ' ', text)
        return text

def enumCast(text, theEnum, logger=None, verbose=True):
    try:
        if isinstance(text, Enum):
            return text
        else:
            return theEnum[text]
    except Exception as e:
        if logger is not None:
            logger.error(str(e), verbose=verbose)
        return None

def enumEquals(a, b):
    if isinstance(a, str) or isinstance(b, str):
        if isinstance(a, Enum):
            a = a.name
        if isinstance(b, Enum):
            b = b.name
    return a == b

def stripAllLines(text, removeBlank=True):
    if text is None or not isinstance(text, str) or text == "":
        return text
    else:
        newText = ""
        for row in text.splitlines():
            current = row.strip()
            if removeBlank and current == "":
                pass
            else:
                newText += current + "\n"
        return newText

def timestampToDate(timestamp, format='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(
        int(timestamp)
    ).strftime(format)

def linearScore(x, x1=0.0, x2=1.0, y1=0.0, y2=1.0, stayBetween0And1=True):
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    y = a * x + b
    if stayBetween0And1:
        if y <= 0.0:
            y = 0.0
        if y >= 1.0:
            y = 1.0
    return y

def camelCaseToUnderscoreCase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
def camelCaseToUnderscoreCaseDict(theDict):
    newDict = {}
    for key, value in theDict.items():
        key = camelCaseToUnderscoreCase(key)
        newDict[key] = value
    return newDict


def reduceDictStr(theDict, max=60, replaceNewLine=False, reduceLists=True, maxElementCountInLists=None):
    if reduceLists and isinstance(theDict, list):
        values = theDict
        if maxElementCountInLists is not None:
            values = values[:maxElementCountInLists]
        newValues = []
        for current in values:
            current = reduceDictStr(current,
                                    max=max,
                                    replaceNewLine=replaceNewLine,
                                    reduceLists=reduceLists,
                                    maxElementCountInLists=maxElementCountInLists)
            newValues.append(current)
        return newValues
    if not isinstance(theDict, dict):
        return theDict
    newDict = {}
    for key, value in theDict.items():
        if isinstance(value, str):
            if replaceNewLine:
                value = value.replace("\n", " ").replace("\r", " ")
            if len(value) > max:
                value = value[0:max-1]
        else:
            value = reduceDictStr(value,
                                    max=max,
                                    replaceNewLine=replaceNewLine,
                                    reduceLists=reduceLists,
                                    maxElementCountInLists=maxElementCountInLists)
        newDict[key] = value
    return newDict

def intersection(lists):
    """
        lists must contain lists of elements or a lists of strings then strings.
    """
    if lists is None or len(lists) == 0 or lists[0] is None:
        return []
    elif len(lists) == 1:
        return lists[0]
    else:
        theIntersection = list(lists[0])
        for current in lists[1:]:
            if current is None:
                theIntersection = []
                break
            else:
                if isinstance(current, str):
                    currentInter = []
                    for el in theIntersection:
                        if el in current:
                            currentInter.append(el)
                    theIntersection = currentInter
                    theIntersection = list(set(theIntersection))
                else:
                    theIntersection = list(set(current).intersection(theIntersection))
        return theIntersection


def lower(text):
    if text is None or not isinstance(text, str):
        return None
    else:
        return text.lower()

def askContinue(message=None, allowExit=True):
    if message is not None:
        print(message)
    toContinue = input("Continue? (Y/n)\n")
    toContinue = toContinue.lower().strip()
    if toContinue != "" and toContinue != "y":
        if allowExit:
            exit()
        else:
            return False
    return True

def dictContains(theDict, key):
    if theDict is None or key is None:
        return False
    if isinstance(theDict, str):
        theDict, key = key, theDict
    if key in theDict and theDict[key] is not None:
        return True
    return False

def dictContainsStr(key, theDict):
    if isinstance(theDict, str):
        theDict, key = key, theDict
    if key in theDict \
    and theDict[key] is not None \
    and isinstance(theDict[key], str) \
    and theDict[key].strip() != "":
        return True
    return False

def getObjectSize(*args, **kwargs):
    return objectSize(*args, **kwargs)
def objectSize(obj, readable=True):
    def sizeof_fmt(num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
    if readable:
        return sizeof_fmt(sys.getsizeof(obj))
    else:
        return sys.getsizeof(obj)

def hash(text):
    return md5(text)

def md5(text):
    theHash = None
    try:
        theHash = hashlib.md5(text)
    except TypeError:
        theHash = hashlib.md5(text.encode("utf-8"))
    else: pass
    if theHash is None:
        return None
    else:
        return theHash.hexdigest()

def dictFirstElement(theDict):
    if not isinstance(theDict, dict):
        return None
    if theDict is None:
        return None
    for key, value in theDict.items():
        return (key, value)

def dictRandomElement(theDict):
    if not isinstance(theDict, dict):
        return None
    if theDict is None:
        return None
    if len(theDict) == 0:
        return None
    randomIndex = getRandomInt(0, len(theDict) - 1)
    currentIndex = 0
    for key, value in theDict.items():
        if currentIndex == randomIndex:
            return (key, value)
        currentIndex += 1




def timestampToArrow(timestampInSec):
    return arrow.get(int(float(timestampInSec)))

def timestampMsToArrow(timestampInMs):
    return arrow.get(int(float(timestampInMs) / 1000.0))



def isDateStr(dateStr):
    try:
        arrow.get(dateStr)
        return True
    except:
        return False


def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)

lastNamesSingleton = None
def getRandomLastname(addInt=True, maxInt=100):
    global lastNamesSingleton
    if lastNamesSingleton is None:
        path = getExecDir(__file__) + "/data/fr-lastnames.txt"
        names = None
        with open(path, 'r') as f:
            names = f.readlines()
        for i in range(len(names)):
            names[i] = names[i].strip()
        lastNamesSingleton = names
    if lastNamesSingleton is None or len(lastNamesSingleton) == 0:
        return getRandomStr()
    name = random.choice(lastNamesSingleton)
    if addInt:
        name = name + "-" + str(getRandomInt(0, maxInt))
    return name

namesSingleton = None
def getRandomName(addInt=True, maxInt=100):
    global namesSingleton
    if namesSingleton is None:
        path = getExecDir(__file__) + "/data/fr-names.txt"
        names = None
        with open(path, 'r') as f:
            names = f.readlines()
        for i in range(len(names)):
            names[i] = names[i].strip()
        namesSingleton = names
    if namesSingleton is None or len(namesSingleton) == 0:
        return getRandomStr()
    name = random.choice(namesSingleton)
    if addInt:
        name = name + "-" + str(getRandomInt(0, maxInt))
    return name

def getRandomEmail(name=None, lastname=None, providers=None):
    if providers is None:
        providers = ["yahoo.com", "gmail.com",
                     "yahoo.fr", "free.fr",
                     "outlook.com", "wanadoo.fr",
                     "hotmail.com"]
    if not isinstance(providers, list):
        providers = [providers]
    provider = random.choice(providers)
    if name is None:
        name = stripAccents(getRandomName(addInt=False))
    name = name.lower()
    if lastname is None:
        lastname = stripAccents(getRandomLastname(addInt=False))
    lastname = lastname.lower()
    name = name + "." + lastname
    name += str(getRandomInt(100))
    if getRandomBool():
        name += str(getRandomInt(100, 1000))
    randomEmail = name + "@" + provider
    randomEmail = randomEmail.replace("-", "")
    return randomEmail

def getRandomStr(digitCount=10, withTimestamp=True):
    result = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(digitCount))
    if withTimestamp:
        timestamp = str(time.time())
        timestamp = timestamp.replace(".", "")
        result = result + "-" + timestamp
    return result

def getRandomFloat(min=0.0, max=1.0, decimalMax=2):
    """
        Warning:
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
    """
    return round(random.uniform(min, max), decimalMax)


class Random:
    def __init__(self):
        self.nextSeed = None

    def setSeed(self, seed):
        self.nextSeed = self.getRandomInt()
        random.seed(seed)

    def resetSeed(self):
        random.seed(self.nextSeed)
        self.nextSeed = None

    def getRandomInt(self, number1=None, number2=None, seed=None, count=1):
        if number1 is None:
            number1 = sys.maxsize
        allRandomInts = []
        if seed is not None:
            nextSeed = getRandomInt(sys.maxsize)
            random.seed(seed)
        if number2 is None:
            theMin = 0
            theMax = number1
        else:
            theMin = number1
            theMax = number2
        for _ in range(count):
            current = random.randint(theMin, theMax)
            allRandomInts.append(current)
        if seed is not None:
            random.seed(nextSeed)
        if len(allRandomInts) == 1:
            return allRandomInts[0]
        else:
            return allRandomInts

    def getRandomBool(self):
        return bool(random.getrandbits(1))

    def getRandomFloat(self, min=0.0, max=1.0, decimalMax=6):
        return round(random.uniform(min, max), decimalMax)


def getRandomInt(number1=None, number2=None, seed=None, count=1):
    if number1 is None:
        number1 = sys.maxsize
    allRandomInts = []
    if seed is not None:
        nextSeed = getRandomInt(sys.maxsize)
        random.seed(seed)
    if number2 is None:
        theMin = 0
        theMax = number1
    else:
        theMin = number1
        theMax = number2
    if isinstance(theMax, float):
        theMax = int(theMax)
    if isinstance(theMin, float):
        theMin = int(theMin)
    for _ in range(count):
        current = random.randint(theMin, theMax)
        allRandomInts.append(current)
    if seed is not None:
        random.seed(nextSeed)
    if len(allRandomInts) == 1:
        return allRandomInts[0]
    else:
        return allRandomInts

def getRandomBool():
    return bool(random.getrandbits(1))

def isIterable(obj, returnTrueForNone=False):
    """
        # To test out of the systemtools-venv:
        isIterable(np.arange(0.0, 0.5, 0.1)

        :example:
        >>> isIterable([])
        True
        >>> isIterable([1])
        True
        >>> isIterable([None])
        True
        >>> isIterable(None)
        False
        >>> isIterable(None, returnTrueForNone=True)
        True
        >>> isIterable(1)
        False
        >>> isIterable({})
        True
        >>> isIterable("a")
        True
        >>> isIterable(random.randint)
        False
    """
    if obj is None:
        if returnTrueForNone:
            return True
        else:
            return False
    try:
        obj = iter(obj)
        return True
    except TypeError:
        return False

def getMinDict(theDict):
    return min(theDict, key=theDict.get)
def getMaxDict(theDict):
    return max(theDict, key=theDict.get)


def countNone(theList):
    return sum(x is None for x in theList)

def removeNone(theList):
    return [x for x in theList if x is not None]

def getFixedLengthQueue(count):
    return collections.deque(count * [None], count)


def dictToTuples(theDict):
    if isinstance(theDict, list):
        return theDict
    tupleList = []
    for key, value in theDict.items():
        tupleList.append((key, value))
    return tupleList


def tuplesToDict(tupleList):
    if isinstance(tupleList, dict):
        return tupleList
    theDict = {}
    for key, value in tupleList:
        theDict[key] = value
    return theDict

def maxTupleList(tupleList, index, getAll=True):
    # Check not none:
    if tupleList is None:
        return None
    # Remove None values:
    tupleList = [x for x in tupleList if x is not None]
    # Check length:
    if len(tupleList) == 0:
        return None
    # Return the max:
    if getAll:
        return max(tupleList, key=lambda item: item[index])
    else:
        return max(tupleList, key=itemgetter(index))[0]



def listMean(l):
    return np.mean(l)

def normalize(theList):
    if theList is None:
        return theList
    else:
        return [float(i) / sum(theList) for i in theList]
#         return [float(i) / max(theList) for i in theList]


def crossValidationChunk(l, partsCount):
    chunkedSet = chunkList(l, partsCount)
    trainingSets = []
    testSets = []
    for i in range(len(chunkedSet)):
        testSets.append(chunkedSet[i])
        currentMatrixTrainingSet = []
        for u in range(len(chunkedSet)):
            if u != i:
                currentMatrixTrainingSet.append(chunkedSet[u])
        currentListTrainingSet = []
        for current in currentMatrixTrainingSet:
            currentListTrainingSet += current
        trainingSets.append(currentListTrainingSet)
    return (trainingSets, testSets)


def sortByValue(theDict, desc=False):
    return sortBy(theDict, desc=desc, index=1)
def sortBy(theDict, desc=False, index=1):
    """
        return a sorted tuple, even if it's a python dict
    """
    data = theDict
    if isinstance(theDict, dict):
        data = theDict.items()
    return sorted(data, key=itemgetter(index), reverse=desc)

def sortByKey(theDict):
    """
        Return an OrderedDict from a dict sorted by keys
    """
    return OrderedDict(sorted(theDict.items()))

def getDictSubElement(theDict, keys):
    """
        This function browse the dict as a tree and return the value in the path
        defined by keys which is a list of dict keys. It return None if it doesn't
        find anything.
    """
    if keys is None or theDict is None:
        return None
    if not isinstance(theDict, dict):
        if len(keys) == 0:
            return theDict
        else:
            return None
    if len(keys) == 0:
        return theDict
    currentKey = keys[0]
    nextKeys = keys[1:]
    if currentKey in theDict:
        return getDictSubElement(theDict[currentKey], nextKeys)
    else:
        return None

def bytesToStr(*args, **kwargs):
    return byteToStr(*args, **kwargs)
def byteToStr(data):
    try:
        data = data.decode("utf-8")
    except AttributeError:
        pass
    return data

def removeNonASCII(str):
    printable = set(string.printable);
    return [x for x in str if x in printable];

def strListToHashCode(strList):
    return hashlib.md5("".join(strList)).hexdigest();

def strToHashCode(str):
#     str = str.encode("utf-8")
    return hashlib.md5(str).hexdigest()

def strToHashCode2(str):
    return hashlib.md5(str).hexdigest()




def isDigit(str):
    return str.isdigit()

def representsFloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def isFloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def isInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def isNumberList(l):
    for el in l:
        if not (isinstance(el, int) or isinstance(el, float)):
            return False
    return True

def isBooleanList(l):
    for el in l:
        if not (isinstance(el, bool)):
            return False
    return True

def listToStr2(obj, indent=4):
    return json.dumps(obj, indent=indent, sort_keys=True)

def reducedLTS(o, amount=25, depth=0):
    try:
        if len(o) > amount:
            tabs = ""
            for i in range(depth):
                tabs += "\t"
            startTabs = tabs[:-1]
            amount = int(amount / 2)
            result = tabs + "[\n"
            for current in o[:amount]:
                result += tabs + "\t" + lts(current, depth=depth + 1) + ",\n"
            result += tabs + "\t" + "..." + ",\n"
            for current in o[-amount:]:
                result += tabs + "\t" + lts(current, depth=depth + 1) + ",\n"
            result = result[:-2]
            result += "\n" + tabs + "]"
            return result
    except: pass
    return "\t" * depth + lts(o, depth=depth)

def lts(*args, **kwargs):
    return listToStr(*args, **kwargs)
def listToStr(l, depth=0, addQuotes=False, maxDepth=None, unknownObjectsToType=False):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    if maxDepth is not None and depth >= maxDepth:
        return tabs + "Depth exceeded"
    if isinstance(l, list) and (isNumberOrBoolList(l)):
        result = "["
        for i in range(len(l)):
            el = l[i]
            result += str(el)
            if i != len(l) - 1:
                result += ", "
        result += "]"
        return result
    if isinstance(l, dict) or "items" in dir(l):
        if unknownObjectsToType and not isinstance(l, dict):
            return tabs + str(type(l))
        result = ""
        result += "{"
        quoteToAdd = ""
        if addQuotes:
            quoteToAdd = '"'
        i = 0
        for key, value in list(l.items()):
            result += "\n"
            result += tabs + "\t" + quoteToAdd + str(key) + quoteToAdd + ": "
            if (isinstance(value, list) or isinstance(value, dict)) and not isNumberOrBoolList(value):
                result += "\n" + tabs + "\t"
            result += listToStr(value, depth + 1, addQuotes=addQuotes, unknownObjectsToType=unknownObjectsToType, maxDepth=maxDepth)
            if (i + 1) < len(l):
                result += ','
            i += 1
        result += "\n" + tabs + "}"
        return result
    elif isinstance(l, list):
        result = ""
        result += "["
        i = 0
        for el in l:
            result += "\n"
            result += tabs + "\t" + listToStr(el, depth + 1, addQuotes=addQuotes, unknownObjectsToType=unknownObjectsToType, maxDepth=maxDepth)
            if (i + 1) < len(l):
                result += ','
            i += 1
        result += "\n" + tabs + "]"
        return result
    else:
        if isinstance(l, str):
            return '"' + l + '"'
        else:
            if unknownObjectsToType:
                return str(type(l))
            else:
                return str(l)

def printLTS(l, *args, loggerFunct=None, **kwargs):
    result = listToStr(l, *args, **kwargs)
    if loggerFunct is not None:
        loggerFunct(result)
    else:
        print(result)


def isNumberOrBoolList(l):
    if len(l) == 0:
        return True
    for el in l:
        if not (isinstance(el, int) or isinstance(el, float) or isinstance(el, bool) or el is None):
            return False
    return True

def dictOfListToListOfDict(data):
    allKeys = list(data.keys())
    newData = []
    listLength = len(data[allKeys[0]])
    for currentIndex in range(listLength):
        newData.append(OrderedDict())
    for currentIndex in range(listLength):
        for currentKey in allKeys:
            newData[currentIndex][currentKey] = data[currentKey][currentIndex]
    return newData

def listOfDictToDictOfList(data):
    newData = OrderedDict()
    for key, value in list(data[0].items()):
        newData[key] = []
    for current in data:
        for key, value in list(current.items()):
            newData[key].append(value)
    return newData

def csvToList(filename, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, folder="./data/", rowLimit=None):
    folder = enhanceDir(folder)
    with open(folder + filename + '.csv', "r") as file:
        c = csv.reader(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
        keys = None
        data = []
        rowCount = 0
        for row in c:
            if rowLimit is not None and rowCount > rowLimit:
                break
            currentDict = None
            if keys is None:
                keys = row
            else:
                rowCount += 1
                currentDict = OrderedDict()
                for currentIndex in range(len(keys)):
                    currentDict[keys[currentIndex]] = row[currentIndex]
                data.append(currentDict)
        return data
    return None

def dictOrListToCSV(filename, data, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, folder="./output/"):
    """
    With these default params, all texts will be quoted. The delimiter is a ';'.
    If there are delimiters in a text, it will be escaped by using 2 double-quotes ('""').
    For example in calc, just set ';' as the column delimiter and '"' as the text delimiter.
    """
    folder = enhanceDir(folder)
    if not isinstance(data, list):
        data = dictOfListToListOfDict(data)
    with open(folder + filename + '.csv', "w") as file:
        c = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
        c.writerow(list(data[0].keys()))
        for currentRow in data:
            currentData = []
            for key, currentCol in list(currentRow.items()):
                currentData.append(currentCol)
            c.writerow(currentData)

        # w = csv.DictWriter(f, my_dict.keys())
    # w.writeheader()
    # w.writerow(my_dict)

    # with open(filename + '.csv', "wb") as f:
        # keys = data[0].keys()
            #  dict_writer = csv.DictWriter(f, keys)
        # dict_writer.writeheader()
        # dict_writer.writerows(data)



def stripAccents(s):
    if isinstance(s, str):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
    else:
        return s

def reduceStr(a,
              removeNumbers=False,
              toLowerCase=True,
              removeAccents=True,
              removePunct=True):
    """
    This funct convert u"-TTé01 fd-hb  /;\\      jdà  \n " to "TTe01 fd hb jda" for exemple
    """
    # if removePointAndComma:
        # a = re.sub(u'[,.]', u' ', a, flags=re.UNICODE)
    if removeAccents:
        a = stripAccents(a)
    if toLowerCase:
        a = a.lower()
    if removeNumbers:
        a = removeAllNumbers(a)

    # remove punct :
    if removePunct:
        # We search all ",1" or ".9"
        allFloatingPoint = re.finditer("[.,]\d", a)
        floatingPointIndex = []
        i = 0
        # We make a replacment list :
        for currentFloatingPoint in allFloatingPoint:
            floatingPointIndex.append\
            (
                ("opkfp" + str(i), currentFloatingPoint.group(0))
            )
            i += 1
        # but ".9" must be replaced by "\.9"
        for i in range(len(floatingPointIndex)):
            floatingPointIndex[i] = (floatingPointIndex[i][0], re.sub('[.]', '\\.', floatingPointIndex[i][1]))
        # We replace all :
        for tag, floatingPoint in floatingPointIndex:
            a = re.sub(floatingPoint, tag, a)
        # We delete punct :
        a = re.sub('[.,;?:!+=\-/_]', ' ', a)
        # And now we have to replace "\.9" by ".9" :
        for i in range(len(floatingPointIndex)):
            floatingPointIndex[i] = (floatingPointIndex[i][0], re.sub('\\\.', '.', floatingPointIndex[i][1]))
        # Now we re-insert all floating points :
        for tag, floatingPoint in floatingPointIndex:
            a = re.sub(tag, floatingPoint, a)

    # remove anything else but ".,;?:!+=\-/_" :
    a = re.sub('[^\w.,;?:!+=\-/_]', ' ', a, flags=re.UNICODE)

    # reduce space :
    a = re.sub('\s+', ' ', a)
    a = a.strip()

    # return the result :
    return a

def addSpaceBeforeUpperCase(text):
    return re.sub('([a-z])([A-Z])', '\\1 \\2', text)

def countOverlap(parsed1, parsed2, ngram):
    print("countOverlap DEPRECATED, pls use NLPTools!")
    if len(parsed1) < ngram or len(parsed2) < ngram:
        return 0
    count = 0
    for i in range(len(parsed1) - (ngram - 1)):
        currentParsed1Ngram = parsed1[i:i + ngram]
        for i in range(len(parsed2) - (ngram - 1)):
            currentParsed2Ngram = parsed2[i:i + ngram]
            if currentParsed1Ngram == currentParsed2Ngram:
                count += 1
    return count

def deleteDuplicate(l):
    return list(set(l))




def strCheck(value):
    return value is not None and isinstance(value, str) and len(value) > 0

def mergeDicts(*dict_args):
    """
    http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
#     result = {}
#     for dictionary in dict_args:
#         if dictionary is not None:
#             result.update(dictionary)
#     return result
    result = {}
    for dictionary in dict_args:
        if dictionary is not None:
            result = {**result, **dictionary}
    return result

def isFrenchDate(s):
    return re.match("^[0-3]\d/[0-1]\d/[1-2]\d{3}$", s) is not None

DATE_FORMAT = Enum("DATE_FORMAT", "datetimeString datetime timestamp arrow arrowString humanize")

def convertDate(readableDate=None, dateFormat=DATE_FORMAT.datetime):
    """
        Warning : utc shift may appear...
        Warning datetime.utcnow() return the utc+0 time
        datetime.now() return the current time in utc+2
    """
    if readableDate is None:
#         print('readableDate is None')
        theDate = datetime.now()
    elif isinstance(readableDate, datetime):
#         print('isinstance(readableDate, datetime)')
        theDate = readableDate
    elif isFloat(readableDate):
#         print('isFloat(readableDate)')
        theDate = datetime.fromtimestamp(float(readableDate))
    elif isDateStr(readableDate):
        if isFrenchDate(readableDate):
            s = readableDate.split("/")
            s = s[2] + "/" + s[1] + "/" + s[0]
            readableDate = s
#         print('isDateStr(readableDate)')
        theDate = arrow.get(readableDate).datetime
    elif isinstance(readableDate, str):
        if isFrenchDate(readableDate):
            s = readableDate.split("/")
            s = s[2] + "/" + s[1] + "/" + s[0]
            readableDate = s
#         print('isinstance(readableDate, str)')
        cal = parsedatetime.Calendar()
#         local_tz = get_localzone()
#         time_struct, parse_status = cal.parseDT(readableDate, tzinfo=local_tz)
        time_struct, parse_status = cal.parse(readableDate)
        theDate = datetime(*time_struct[:6])
    else:
        return None
#     local_tz = get_localzone()
#     print(local_tz)
#     local_now = theDate.replace(tzinfo=pytz.utc).astimezone(local_tz)
#     theDate = local_now
    timestamp = theDate.timestamp()
    if dateFormat == DATE_FORMAT.datetime:
        return theDate
    elif dateFormat == DATE_FORMAT.timestamp:
        return timestamp
    elif dateFormat == DATE_FORMAT.datetimeString:
        return str(theDate)
    elif dateFormat == DATE_FORMAT.humanize:
        return arrow.get(theDate).humanize() # locale='fr_fr'
    elif dateFormat == DATE_FORMAT.arrow:
        return timestampToArrow(timestamp)
    elif dateFormat == DATE_FORMAT.arrowString:
        return str(timestampToArrow(timestamp))
    else:
        return None


def weAreBefore(readableDate):
    d = convertDate(readableDate, dateFormat=DATE_FORMAT.timestamp)
    return time.time() < d
def weAreAfter(*args, **kwargs):
    return not weAreBefore(*args, **kwargs)

def listSubstract(a, b):
    if a is None:
        return []
    elif b is None:
        return a
    else:
        return [item for item in a if item not in b]


def test1():
    for readableDate in [
                        None,
                        datetime.now(),
                        datetime.now().timestamp(),
                        1506813088.541,
                        "1506813088",
                        "2017-10-22 14:11:10.800615",
                        "2017-10-22T14:11:10+00:00",
                        "2 mins ago",
                        "None",
                        "2017-10-01 01:23:35",
                        "aaa",
                        "2017-09-30T23:11:28+00:00",
                        "2 days ago", "in 2 days", "in 40 years",
                         "tomorrow at 6am", "next moday at noon",
                        "2 min ago", "3 weeks ago", "1 month ago",
                        "in 40 years at the 1st january 11am",
                        "1506813088.0",
                        1506813088.45247, "1506813088.45247",
                        1506813088,
                        "iusqhdfusdgfb jsdf dsgf usdbg",
                        ]:
        print(readableDate)
        for currentDateFormat in DATE_FORMAT:
            print(str(convertDate(readableDate, dateFormat=currentDateFormat)) + "\t\t" + str(currentDateFormat))
        print()
        print()



def test2():
        dateObj = datetime.now()
        dateObj = 'now'
        print(convertDate(dateObj, dateFormat=DATE_FORMAT.datetime))
        print(convertDate(dateObj, dateFormat=DATE_FORMAT.humanize))

def testPartList():
    lists = \
    [
#         [],
#         None,
#         [1],
#         [1, 2, 3],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    ]
    for current in lists:
        printLTS(list(partListDeprecated(current, 0)))
        printLTS(list(partListDeprecated(current, 1)))
        printLTS(list(partListDeprecated(current, 2)))
        printLTS(list(partListDeprecated(current, 3)))
        printLTS(list(partListDeprecated(current, 4)))


def chunkList(l, partsCount):
    print("DEPRECATED, use chunks instead!")
    chunkedList = []
    partsItemNumber = int(math.ceil(float(len(l)) / float(partsCount)))
    for i in range(partsCount):
        left = l[:partsItemNumber]
        right = l[partsItemNumber:]
        chunkedList.append(left)
        l = right
    return chunkedList
def partListDeprecated(*args, **kwargs):
    return chunksDeprecated(*args, **kwargs)
def chunksDeprecated(*args, **kwargs):
    return list(chunksYielderDepprecated(*args, **kwargs))
def chunksYielderDepprecated(l, n):
    """Yield successive n-sized chunks from l."""
    if l is None:
        yield None
    elif len(l) <= 1:
        yield l
    elif n <= 1:
        yield l
    else:
        n = math.ceil(len(l) / n)
        if n >= len(l):
            for current in l:
                yield current
        else:
            for i in range(0, len(l), n):
                yield l[i:i + n]

def chunk(*args, **kwargs):
    return chunks(*args, **kwargs)
def chunks(*args, **kwargs):
    return list(chunksYielder(*args, **kwargs))
def chunksYielder(l, n):
    """Yield successive n-sized chunks from l."""
    if l is None:
        return []
    for i in range(0, len(l), n):
        yield l[i:i + n]

def splitMaxSized(l, batchMaxSize):
    """
        Split a list in multiple parts in such a way that each part has a max size of batchMaxSize
    """
    batchCount = 1
    if batchMaxSize is not None and batchMaxSize > 0:
        batchCount = math.ceil(len(l) / batchMaxSize)
    return split(l, batchCount)

def split(l, n):
    """
        Split a list in n parts
    """
    if l is None:
        return []
#     avg = len(l) / float(n)
#     out = []
#     last = 0.0
#
#     while last < len(l):
#         out.append(l[int(last):int(last + avg)])
#         last += avg
#
#     return out
    return [l[i::n] for i in range(n)]

def dictHash(*args, **kwargs):
    return objectAsKey(*args, **kwargs)
def objectHash(*args, **kwargs):
    return objectAsKey(*args, **kwargs)
def objectAsKey(o):
    """
        :example:
        >>> objectAsKey([1, {"c": {"a", 1, "t"}, "b": [2, 1], "a": "t"}, {}, [], None])
        '[1, [[a, t], [b, [2, 1]], [c, [1, a, t]]], [], [], None]'
    """
    if isinstance(o, list):
        newO = []
        for current in o:
            newO.append(objectAsKey(current))
        result = "["
        for current in newO:
            result += str(current) + ", "
        if len(o) > 0:
            result = result[:-2]
        result += "]"
        return str(result)
    elif isinstance(o, set):
        newO = []
        for current in o:
            newO.append(str(current))
        newO = sorted(newO)
        return objectAsKey(newO)
    elif isinstance(o, tuple):
        o = list(o)
        return objectAsKey(o)
    elif isinstance(o, dict):
        o = list(sortByKey(o).items())
        return objectAsKey(o)
    return str(o)

if __name__ == '__main__':
    o = [1, {"c": {"a", 1, "t"}, "b": [2, 1], "a": "t"}, {}, [], None]
    print(reducedLTS(o, 4))

    # for i in range(1000):
    #     print(getRandomEmail(name="jean", lastname="aaaaa", providers=None))
    # exit()
#     print(normalize([0.5, 0.5, 1.0, 2.0]))
#     print(normalize([0.2, 0.2, 0.4, 0.2]))
#     print(normalize([20, 20, 40, 20]))
#     print(normalize([10, 30, 40, 50]))
#     print(normalize([0.1, 0.1, 0.2]))
#     test1()
#     test2()
#     print(datetime.now())
#     testPartList()


#
#     dicts = \
#     [
#         {"a": 1, "b": 2},
#         {"b": 2, "a": 1},
#         {"a": 1},
#         {},
#         None,
#         {"b": 2, "a": 1, "c": 3},
#         {"b": 2, "a": 1, "c": 3, "d": 4},
#     ]
#
#
#     for i in range(1000):
#         for currentDict in dicts:
#             printLTS(dictRandomElement(currentDict))
#

#     for i in range(100):
#         print(getRandomName())



#     theDict = {}
#     for i in range(1000):
#         theDict[getRandomInt(0, 1000000)] = getRandomInt(0, 1000000)
#     print(objectSize())
#     test2()

    # l = list(range(100))
    # printLTS(chunksDeprecated(l, 6))




# We don't need this because "test"[0:30] doesn't raise any exception...
# def cut(theString, minIndex, maxIndex=None):
#     """
#         Return the same string truncated in [minIndex, maxIndex]
#         These index (at the border) include the corresponding letter
#         If max is too long, it will be replaced by -1
#         If max is None, max become min et min become 0
#
#         :example:
#         >>> cut("test", 2)
#         "tes"
#         >>> cut("test", 2, -1)
#         "st"
#         >>> cut("test", 0, -1)
#         "test"
#         >>> cut("test", -2)
#         "tes"
#         >>> cut("test", -2, -1)
#         "st"
#         >>> cut(None, -2, -1)
#         None
#         >>> cut("", -2, -1)
#         ""
#         >>> cut(None, 1)
#         None
#         >>> cut("", 1)
#         ""
#     """
#     if maxIndex is None:
#         maxIndex = minIndex
#         minIndex = 0
#     theStringLen = len(theString)
#     if maxIndex > theStringLen:
#         maxIndex = theStringLen
#     return theString[minIndex:maxIndex]


