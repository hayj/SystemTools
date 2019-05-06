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
import getpass
from pathlib import Path
import socket
from systemtools.number import digitalizeIntegers
from operator import itemgetter

def decomposePath(path):
    """
        :example:
        >>> decomposePath(None)
        >>> decomposePath("")
        >>> decomposePath(1)
        >>> decomposePath("truc")
        ('', 'truc', '', 'truc')
        >>> decomposePath("truc.txt")
        ('', 'truc', 'txt', 'truc.txt')
        >>> decomposePath("/home/truc.txt")
        ('/home/', 'truc', 'txt', 'truc.txt')
        >>> decomposePath("/home/truc.txt.bz2")
        ('/home/', 'truc.txt', 'bz2', 'truc.txt.bz2')
        >>> decomposePath("/truc.txt.bz2")
        ('/', 'truc.txt', 'bz2', 'truc.txt.bz2')
        >>> decomposePath("./truc.txt.bz2")
        ('./', 'truc.txt', 'bz2', 'truc.txt.bz2')
        >>> decomposePath(".truc.txt.bz2")
        ('', '.truc.txt', 'bz2', '.truc.txt.bz2')
    """
    if path is None or type(path) is not str or len(path) == 0:
        return None
    filenameExt = path.split("/")[-1]
    dir = path[0:-len(filenameExt)]
    filename = ".".join(filenameExt.split(".")[0:-1])
    ext = filenameExt.split(".")[-1]
    if len(filename) == 0 and len(ext) > 0:
        filename, ext = ext, filename
    return (dir, filename, ext, filenameExt)

def decomposePath2(path):
    """
        :example:
        >>> decomposePath(None)
        >>> decomposePath("")
        >>> decomposePath(1)
        >>> decomposePath("truc")
        ('', 'truc', '', 'truc')
        >>> decomposePath("truc.txt")
        ('', 'truc', 'txt', 'truc.txt')
        >>> decomposePath("/home/truc.txt")
        ('/home/', 'truc', 'txt', 'truc.txt')
        >>> decomposePath("/home/truc.txt.bz2")
        ('/home/', 'truc.txt', 'bz2', 'truc.txt.bz2')
        >>> decomposePath("/truc.txt.bz2")
        ('/', 'truc.txt', 'bz2', 'truc.txt.bz2')
        >>> decomposePath("./truc.txt.bz2")
        ('./', 'truc.txt', 'bz2', 'truc.txt.bz2')
        >>> decomposePath(".truc.txt.bz2")
        ('', '.truc.txt', 'bz2', '.truc.txt.bz2')
    """
    if path is None or type(path) is not str or len(path) == 0:
        return None
    filenameExt = path.split("/")[-1]
    dir = path[0:-len(filenameExt)]
    if len(dir) > 1 and dir[-1] == "/":
        dir = dir[:-1]
    filename = ".".join(filenameExt.split(".")[0:-1])
    ext = filenameExt.split(".")[-1]
    if len(filename) == 0 and len(ext) > 0:
        filename, ext = ext, filename
    return (dir, filename, ext, filenameExt)

def enhanceDir(path):
    if path[-1] != '/':
        path += '/'
    return path

def removeLastSlash(text):
    if isinstance(text, str):
        if text[-1] == '/':
            return text[0:-1]
    return text

def getCurrentDir():
    return os.getcwd()

def pathToAbsolute(path):
    if len(path) > 0 and path[0] != "/":
        path = getCurrentDir() + "/" + path
    return path

def isFile(filePath):
    filePath = pathToAbsolute(filePath)
#     print filePath
    return os.path.isfile(filePath)

def isDir(dirPath):
    dirPath = pathToAbsolute(dirPath)
    return os.path.isdir(dirPath)

def getDir(filePath):
    return os.path.dirname(os.path.abspath(filePath))

def parentDir(*args, **kwargs):
    return getParentDir(*args, **kwargs)
def getParentDir(path, depth=1):
    for i in range(depth):
        path = os.path.abspath(os.path.join(path, os.pardir))
    return path

def absPath(path):
    return os.path.abspath(path)

# Deprecated:
def getRootDirectory(*args, **kwargs):
    return getExecDirectory(*args, **kwargs)
def getExecDir(*args, **kwargs):
    return getExecDirectory(*args, **kwargs)
def execPath(*args, **kwargs):
    return getExecDirectory(*args, **kwargs)
def execDir(*args, **kwargs):
    return getExecDirectory(*args, **kwargs)
def getExecDirectory(_file_=None):
    """
    Get the directory of the root execution file
    Can help: http://stackoverflow.com/questions/50499/how-do-i-get-the-path-and-name-of-the-file-that-is-currently-executing
    For eclipse user with unittest or debugger, the function search for the correct folder in the stack
    You can pass __file__ (with 4 underscores) if you want the caller directory
    """
    # If we don't have the __file__ :
    if _file_ is None:
        # We get the last :
        rootFile = inspect.stack()[-1][1]
        folder = os.path.abspath(rootFile)
        # If we use unittest :
        if ("/pysrc" in folder) and ("org.python.pydev" in folder):
            previous = None
            # We search from left to right the case.py :
            for el in inspect.stack():
                currentFile = os.path.abspath(el[1])
                if ("unittest/case.py" in currentFile) or ("org.python.pydev" in currentFile):
                    break
                previous = currentFile
            folder = previous
        # We return the folder :
        return os.path.dirname(folder)
    else:
        # We return the folder according to specified __file__ :
        return os.path.dirname(os.path.realpath(_file_))

def getWorkingDirectory(*args, **kwargs):
    return tmpDir(*args, **kwargs)
def getTmpDir(*args, **kwargs):
    return tmpDir(*args, **kwargs)
def tmpPath(*args, **kwargs):
    return tmpDir(*args, **kwargs)
def getTmpPath(*args, **kwargs):
    return tmpDir(*args, **kwargs)
def tmpDir(_file_=None, subDir=None):
    """
        _file_ and subDir can be switched
        The rule is _file_ must finish by ".py"
    """
    # First we switch both parameters if needed:
    if _file_ is not None and _file_[-3:] != ".py":
        subDir, _file_ = _file_, subDir
    # Then we modified subDir if needed:
    if subDir is None:
        subDir = ""
    elif not subDir.startswith("/"):
            subDir = "/" + subDir
    # Finally we get the root path:
    if _file_ is None:
        rootPath = homeDir()
    else:
        rootPath = execDir(_file_)
    # And we get the tmp directory:
    workingPath = rootPath + "/tmp" + subDir
    # Add the tmp directory if not exists :
    os.makedirs(workingPath, exist_ok=True)
    return workingPath

# Deprecated:
def getUtilDirectory():
    return os.path.dirname(os.path.realpath(__file__));

class GlobSortEnum():
    (
        AUTO,
        MTIME,
        NAME,
        SIZE,
        NUMERICAL_NAME
    ) = list(range(5))


def sortedGlob(regex, caseSensitive=True, sortBy=GlobSortEnum.AUTO, reverse=False):
    """
        See the README

        :params:
        regex : string
            the pattern used to find files or folders
        caseSensitive : boolean
            set it as False if you don't want to take care of the case
        sortBy : enum item
            can be GlobSortEnum.<MTIME|NAME|SIZE|NUMERICAL_NAME>,
            the last one is the same as name but take into account the last number in the given path numbers
            (e.g. test1.txt < test10.txt)
        reverse : boolean
            set it as True if you want to reverse the order
    """
    def getFileNum(fileName):
        """
            :example:
            >>> getFileNum(None)
            >>> getFileNum("truc")
            >>> getFileNum("truc.md")
            >>> getFileNum("10truc2.4md")
            10
            >>> getFileNum("505.bz2")
            505
            >>> getFileNum("505.bz2")
            505
        """
        if fileName is None or len(fileName) == 0:
            return None
        result = re.findall("([0-9]+)", fileName)
        if result is not None:
            try:
                theInt = result[-1]
                return int(theInt)
            except IndexError as e:
                return None
        return None

    # case insensitive glob function :
    def insensitiveGlob(pattern):
        def either(c):
            return '[%s%s]'%(c.lower(), c.upper()) if c.isalpha() else c
        return glob.glob(''.join(map(either, pattern)))

    # Handle case insentive param :
    if caseSensitive:
        paths = glob.glob(regex)
    else:
        paths = insensitiveGlob(regex)

    # Sort the result :
    if sortBy == GlobSortEnum.AUTO:
        # First we replace all integers by "000000012" for "12" for example:
        totalDigits = 100
        data = []
        for text in paths:
            data.append((text, digitalizeIntegers(text)))
            data = sorted(data, key=itemgetter(1))
        paths = [x for x, y in data]
    elif sortBy == GlobSortEnum.NAME:
        print("DEPRECATED GlobSortEnum.NAME, use GlobSortEnum.AUTO instead")
        paths.sort(reverse=reverse)
    elif sortBy == GlobSortEnum.MTIME:
        paths.sort(key=os.path.getmtime, reverse=reverse)
    elif sortBy == GlobSortEnum.SIZE:
        paths.sort(key=os.path.getsize, reverse=reverse)
    elif sortBy == GlobSortEnum.NUMERICAL_NAME:
        print("DEPRECATED GlobSortEnum.NUMERICAL_NAME, use GlobSortEnum.AUTO instead")
        paths.sort(key=getFileNum, reverse=reverse)

    return list(paths)


def homePath(*args, **kwargs):
    return homeDir(*args, **kwargs)

def nosaveDir():
    if isDir("/NoSave"):
        return "/NoSave"
    elif isDir(homeDir() + "/NoSave"):
        return homeDir() + "/NoSave"
    else:
        print("No NoSave dir found.")
        return tmpDir()

def homeDir():
    if isDir("/hosthome"):
        return "/hosthome"
    else:
        return str(Path.home())


def getDataPath(*args, **kwargs):
    return dataPath(*args, **kwargs)
def getDataDir(*args, **kwargs):
    return dataPath(*args, **kwargs)
def dataDir(*args, **kwargs):
    return dataPath(*args, **kwargs)
def dataPath(defaultDirName="Data"):
    def isHostname(hostname):
        return socket.gethostname().startswith(hostname)
    if isDir("/NoSave"):
        return "/NoSave/Data"
    elif isDir(homeDir() + "/NoSave"):
        return "/users/modhel-nosave/hayj/" + defaultDirName
    else:
        return homeDir() + "/" + defaultDirName

def sortedWalk():
    pass # TODO

if __name__ == '__main__':
#     print(tmpDir(subDir="test"))
    print(sortedGlob(dataDir() + "/*"))







