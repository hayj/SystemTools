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

def timestampToDate(timestamp):
    return datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')

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

def reduceDictStr(theDict, max=40, replaceNewLine=False, reduceLists=False, maxElementCountInLists=1):
    if reduceLists and isinstance(theDict, list):
        values = theDict[:maxElementCountInLists]
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

def strip(text):
    if text is None or not isinstance(text, str):
        return None
    else:
        return text.strip()

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

def getRandomEmail():
    providers = ["yahoo.com"] * 3 + ["gmail.com", "yahoo.fr", "free.fr"]
    provider = random.choice(providers)
    name = stripAccents(getRandomName(addInt=False)).lower()
    lastname = stripAccents(getRandomLastname(addInt=False)).lower()
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


def truncateFloat(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return float('{0:.{1}f}'.format(f, n))
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))

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

def floatAsReadable(f):
    """
        source https://stackoverflow.com/questions/8345795/force-python-to-not-output-a-float-in-standard-form-scientific-notation-expo
    """
    _ftod_r = re.compile(br'^(-?)([0-9]*)(?:\.([0-9]*))?(?:[eE]([+-][0-9]+))?$')
    """Print a floating-point number in the format expected by PDF:
    as short as possible, no exponential notation."""
    s = bytes(str(f), 'ascii')
    m = _ftod_r.match(s)
    if not m:
        raise RuntimeError("unexpected floating point number format: {!a}"
                           .format(s))
    sign = m.group(1)
    intpart = m.group(2)
    fractpart = m.group(3)
    exponent = m.group(4)
    if ((intpart is None or intpart == b'') and
        (fractpart is None or fractpart == b'')):
        raise RuntimeError("unexpected floating point number format: {!a}"
                           .format(s))

    # strip leading and trailing zeros
    if intpart is None: intpart = b''
    else: intpart = intpart.lstrip(b'0')
    if fractpart is None: fractpart = b''
    else: fractpart = fractpart.rstrip(b'0')

    result = None

    if intpart == b'' and fractpart == b'':
        # zero or negative zero; negative zero is not useful in PDF
        # we can ignore the exponent in this case
        result = b'0'

    # convert exponent to a decimal point shift
    elif exponent is not None:
        exponent = int(exponent)
        exponent += len(intpart)
        digits = intpart + fractpart
        if exponent <= 0:
            result = sign + b'.' + b'0'*(-exponent) + digits
        elif exponent >= len(digits):
            result = sign + digits + b'0'*(exponent - len(digits))
        else:
            result = sign + digits[:exponent] + b'.' + digits[exponent:]

    # no exponent, just reassemble the number
    elif fractpart == b'':
        result = sign + intpart # no need for trailing dot
    else:
        result = sign + intpart + b'.' + fractpart

    return result.decode("utf-8")


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


def trim(str):
    pattern = re.compile(r'\s+')
    str = re.sub(pattern, ' ', str)
    str = str.strip();
    return str


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



def representsInt(s, acceptRoundedFloats=False):
    """
        This function return True if the given param (string or float) represents a int

        :Example:
        >>> representsInt(1)
        True
        >>> representsInt("1")
        True
        >>> representsInt("a")
        False
        >>> representsInt("1.1")
        False
        >>> representsInt(1.1)
        False
        >>> representsInt(42.0, acceptRoundedFloats=True)
        True
        >>> representsInt("42.0", acceptRoundedFloats=True)
        True
    """

    if isinstance(s, float):
        if acceptRoundedFloats:
            return s.is_integer()
    else:
        if acceptRoundedFloats:
            try:
                s = float(s)
                return representsInt(s, acceptRoundedFloats=acceptRoundedFloats)
            except ValueError:
                return False
        else:
            try:
                int(s)
                return True
            except ValueError:
                return False
    return False

def listToStr2(obj, indent=4):
    return json.dumps(obj, indent=indent, sort_keys=True)

def lts(*args, **kwargs):
    return listToStr(*args, **kwargs)
def listToStr(l, depth=0):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    if isinstance(l, list) and (isNumberOrBoolList(l)):
        result = "["
        for i in range(len(l)):
            el = l[i]
            result += str(el)
            if i != len(l) - 1:
                result += ", "
        result += "]"
        return result
    if isinstance(l, dict):
        result = ""
        result += "{"
        i = 0
        for key, value in list(l.items()):
            result += "\n"
            result += tabs + "\t" + str(key) + ": "
            if (isinstance(value, list) or isinstance(value, dict)) and not isNumberOrBoolList(value):
                result += "\n" + tabs + "\t"
            result += listToStr(value, depth + 1)
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
            result += tabs + "\t" + listToStr(el, depth + 1)
            if (i + 1) < len(l):
                result += ','
            i += 1
        result += "\n" + tabs + "]"
        return result
    else:
        if isinstance(l, str):
            return '"' + l + '"'
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


def removeCommasBetweenDigits(text):
    """
        :example:
        >>> removeCommasBetweenDigits("sfeyv dsf,54dsf ef 6, 6 zdgy 6,919 Photos and 3,3 videos6,")
        'sfeyv dsf,54dsf ef 6, 6 zdgy 6919 Photos and 33 videos6,'
    """
    if text is None:
        return None
    else:
        return re.sub(r"([0-9]),([0-9])", "\g<1>\g<2>", text)

def getAllNumbers(text, removeCommas=False):
    if text is None:
        return None
    if removeCommas:
        text = removeCommasBetweenDigits(text)
    allNumbers = []
    if len(text) > 0:
        # Remove space between digits :
        spaceNumberExists = True
        while spaceNumberExists:
            text = re.sub('(([^.,0-9]|^)[0-9]+) ([0-9])', '\\1\\3', text, flags=re.UNICODE)
            if re.search('([^.,0-9]|^)[0-9]+ [0-9]', text) is None:
                spaceNumberExists = False
        numberRegex = '[-+]?[0-9]+[.,][0-9]+|[0-9]+'
        allMatchIter = re.finditer(numberRegex, text)
        if allMatchIter is not None:
            for current in allMatchIter:
                currentFloat = current.group()
                currentFloat = re.sub("\s", "", currentFloat)
                currentFloat = re.sub(",", ".", currentFloat)
                currentFloat = float(currentFloat)
                if currentFloat.is_integer():
                    allNumbers.append(int(currentFloat))
                else:
                    allNumbers.append(currentFloat)
    return allNumbers

def removeAllNumbers(text):
    if text is None:
        return None
    if len(text) == 0:
        return ""
    # Remove space between digits :
    spaceNumberExists = True
    while spaceNumberExists:
        text = re.sub('([0-9]) ([0-9])', '\\1\\2', text, flags=re.UNICODE)
        if re.search('[0-9] [0-9]', text) is None:
            spaceNumberExists = False
    numberRegex = '[-+]?[0-9]+[.,][0-9]+|[0-9]+'
    numberExists = True
    while numberExists:
        text = re.sub(numberRegex, "", text)
        if re.search(numberRegex, text) is None:
            numberExists = False

    return text.strip()

def getFirstNumber(text, *args, **kwargs):
    result = getAllNumbers(text, *args, **kwargs)
    if result is not None and len(result) > 0:
        return result[0]
    return None

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
#         print('isDateStr(readableDate)')
        theDate = arrow.get(readableDate).datetime
    elif isinstance(readableDate, str):
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
    print("DEPRECATED, use chunksDeprecated instead!")
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
    """Yield successive n-sized chunksDeprecated from l."""
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
    """Yield successive n-sized chunksDeprecated from l."""
    if l is None:
        return []
    for i in range(0, len(l), n):
        yield l[i:i + n]


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

if __name__ == '__main__':

    for i in range(1000):
        print(getRandomEmail())
    exit()
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

    l = list(range(100))
    printLTS(chunksDeprecated(l, 6))




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


