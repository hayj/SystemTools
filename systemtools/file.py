# coding: utf-8

import os, errno
import shutil
import re
import time
from enum import Enum
import pickle
import string
from systemtools.location import isFile, getDir, isDir, sortedGlob, decomposePath, tmpDir, homeDir
from systemtools.basics import getRandomStr
import subprocess, zipfile
from distutils.dir_util import copy_tree
import requests
import xtract


class TIMESPENT_UNIT(Enum):
    DAYS = 1
    HOURS = 2
    MINUTES = 3
    SECONDS = 4
def getLastModifiedTimeSpent(path, timeSpentUnit=TIMESPENT_UNIT.HOURS):
    diff = time.time() - os.path.getmtime(path)
    if timeSpentUnit == TIMESPENT_UNIT.SECONDS:
        return diff
    diff = diff / 60.0
    if timeSpentUnit == TIMESPENT_UNIT.MINUTES:
        return diff
    diff = diff / 60.0
    if timeSpentUnit == TIMESPENT_UNIT.HOURS:
        return diff
    diff = diff / 24.0
    if timeSpentUnit == TIMESPENT_UNIT.DAYS:
        return diff

def purgeOldFiles(pattern, maxTimeSpent, timeSpentUnit=TIMESPENT_UNIT.SECONDS):
    allPlugins = sortedGlob(pattern)
    for current in allPlugins:
        timeSpent = getLastModifiedTimeSpent(current, timeSpentUnit)
        if timeSpent > maxTimeSpent:
            removeFile(current)

def strToFileName(*args, **kwargs):
    return strToFilename(*args, **kwargs)

def strToFilename(text):
    """

    https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    """
    text = text.replace(" ", "_")
    valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in text if c in valid_chars)

def serialize(obj, path):
    with open(path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def deserialize(path):
    with open(path, 'rb') as handle:
        return pickle.load(handle)

def copyDir(src, dst):
    if not (src.startswith("/") and src.startswith("/")):
        raise Exception("Pls give absolute path.")
    if src.count("/") < 2 or dst.count("/") < 2:
        raise Exception("Pls give a deep folder (by security).")
    (dir, filename, ext, filenameExt) = decomposePath(src)
    if dir[-1] != "/":
        dir += "/"
    dir = dir + filenameExt
    if dir != src or not isDir(dir):
        raise Exception("Pls give a right dir path.")
    dirName = dir.split("/")[-1]
    return copy_tree(src, dst + "/" + dirName)

def copyFile(src, dst):
    return shutil.copyfile(src, dst)

def getAllNumbers(text):
    """
        This function is a copy of systemtools.basics.getAllNumbers
    """
    if text is None:
        return None
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


def mkdir(path):
    mkdirIfNotExists(path)

def mkdirIfNotExists(path):
    """
        This function make dirs recursively like mkdir -p in bash
    """
    os.makedirs(path, exist_ok=True)

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def replaceInFile(path, listSrc, listRep):
    with open(path, 'r') as f :
        filedata = f.read()
    for i in range(len(listSrc)):
        src = listSrc[i]
        rep = listRep[i]
        filedata = filedata.replace(src, rep)
    with open(path, 'w') as f:
        f.write(filedata)

def fileExists(filePath):
    return os.path.exists(filePath)

def globRemove(globPattern):
    filesPaths = sortedGlob(globPattern)
    removeFiles(filesPaths)

def removeFile(path):
    if not isinstance(path, list):
        path = [path]
    for currentPath in path:
        try:
            os.remove(currentPath)
        except OSError:
            pass
def removeFiles(path):
    removeFile(path)
def removeAll(path):
    removeFile(path)

def fileToStr(path, split=False, encoding=None):
    if split:
        return fileToStrList(path)
    else:
        with open(path, 'r', encoding=encoding) as myfile:
            data = myfile.read()
        return data

def fileToStrList_old(path, strip=True):
    data = fileToStr(path)
    if strip:
        data = data.strip()
    return data.splitlines()

def fileToStrList(*args, removeDuplicates=False, **kwargs):
    result = fileToStrListYielder(*args, **kwargs)
    if removeDuplicates:
        return list(set(list(result)))
    else:
        return list(result)

def basicLog(text, logger, verbose):
    if verbose:
        if text is not None and text != "":
            if logger is None:
                print(text)
            else:
                logger.info(text)

def fileToStrListYielder(path,
                         strip=True,
                         skipBlank=True,
                         commentStart="###",
                         logger=None,
                         verbose=False):

    if path is not None and isFile(path):
        commentCount = 0
        with open(path) as f:
            for line in f.readlines():
                isComment = False
                if strip:
                    line = line.strip()
                if commentStart is not None and len(commentStart) > 0 and line.startswith(commentStart):
                    commentCount += 1
                    isComment = True
                if not isComment:
                    if skipBlank and len(line) == 0:
                        pass
                    else:
                        yield line
        if commentCount > 0:
            basicLog("We found " + str(commentCount) + " comments in " + path, logger, verbose)
    else:
        basicLog(str(path) + " file not found.", logger, verbose)


def removeIfExists(path):
    try:
        os.remove(path)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
def removeIfExistsSecure(path, slashCount=5):
    if path.count('/') >= slashCount:
        removeIfExists(path)

def removeDir(*args, **kwargs):
    return removeTreeIfExists(*args, **kwargs)
def removeTreeIfExists(path):
    return shutil.rmtree(path, True)
def removeDirSecure(*args, **kwargs):
    return removeTreeIfExistsSecure(*args, **kwargs)
def removeTreeIfExistsSecure(path, slashCount=5):
    if path.count('/') >= slashCount:
        return removeTreeIfExists(path)
    return None

def strListToTmpFile(theList, *args, **kwargs):
    text = ""
    for current in theList:
        text += current + "\n"
    return strToTmpFile(text, *args, **kwargs)

def strToTmpFile(text, name=None, ext="", addRandomStr=False, *args, **kwargs):
    if text is None:
        text = ""
    if ext is None:
        ext = ""
    if ext != "":
        if not ext.startswith("."):
            ext = "." + ext
    if name is None:
        name = getRandomStr()
    elif addRandomStr:
        name += "-" + getRandomStr()
    path = tmpDir(*args, **kwargs) + "/" + name + ext
    strToFile(text, path)
    return path

def strToFileAppend(*args, **kwargs):
    appendFile(*args, **kwargs)
def appendToFile(*args, **kwargs):
    appendFile(*args, **kwargs)
def appendStrToFile(*args, **kwargs):
    appendFile(*args, **kwargs)
def appendFile(text, path, addBreakLine=True):
    if text is None:
        return
    if isinstance(text, list):
        text = "\n".join(text)
    with open(path, "a") as f:
        if addBreakLine:
            text = "\n" + str(text)
        f.write(text)




def strListToFile(*args, **kwargs):
    strToFile(*args, **kwargs)
def strToFile(text, path):
#     if not isDir(getDir(path)) and isDir(getDir(text)):
#         path, text = text, path
    if isinstance(text, list):
        text = "\n".join(text)
    textFile = open(path, "w")
    textFile.write(text)
    textFile.close()

def normalizeNumericalFilePaths(globRegex):
    """
        This function get a glob path and rename all file1.json file2.json ... file20.json
        to file01.json file02.json ... file20.json to better sort the folder by file names
    """
    # We get all paths:
    allPaths = sortedGlob(globRegex)
    allNumbers = []
    # We get all ints:
    for path in allPaths:
        # Get the filename without extension:
        (dir, filename, ext, filenameExt) = decomposePath(path)
        # Get all numbers:
        currentNumbers = getAllNumbers(filename)
        # Check if we have a int first:
        if currentNumbers is None or len(currentNumbers) == 0:
            print("A filename has no number.")
            return False
        firstNumber = currentNumbers[0]
        if not isinstance(firstNumber, int):
            print("A filename has no float as first number.")
            return False
        # Add it in the list:
        allNumbers.append(firstNumber)
    # Get the max int:
    maxInt = max(allNumbers)
    # Calculate the nmber of digit:
    digitCountHasToBe = len(str(maxInt))
    # Replace all :
    i = 0
    for i in range(len(allNumbers)):
        currentPath = allPaths[i]
        (dir, filename, ext, filenameExt) = decomposePath(currentPath)
        currentInt = allNumbers[i]
        currentRegex = "0*" + str(currentInt)
        zerosCountToAdd = digitCountHasToBe - len(str(currentInt))
        zerosStr = "0" * zerosCountToAdd
        newFilename = re.sub(currentRegex, zerosStr + str(currentInt), filename, count=1)
        newFilename = dir + newFilename + "." + ext
        if currentPath != newFilename:
            os.rename(currentPath, newFilename)
            print(newFilename + " done.")
        i += 1
    return True


def encryptFile(path, key, text=None, ext=".encrypted.zip", remove=False, logger=None, verbose=True):
    """
        This function encrypt a file, if you give text in `text` parameter,
        the function will create the file.
        Return True if all is ok.
    """
    try:
        if text is not None:
            strToFile(text, path)
        rc = subprocess.call(['7z', 'a', '-p' + key, '-y', path + ext, path], stdout=open(os.devnull, 'wb'))
        if remove:
            removeFile(path)
        return True
    except Exception as e:
        if verbose:
            if logger is None:
                print(str(e))
            else:
                logger.error(str(e))
        return False

def decryptFile(path, key, ext=".encrypted.zip", remove=False, logger=None, verbose=True):
    """
        This function decrypt a file and return the text
    """
    try:
        (dir, _, _, _) = decomposePath(path)
        key = str.encode(key)
        if path[-len(ext):] != ext:
            decryptedFilePath = path
            cryptedFilePath = decryptedFilePath + ext
        else:
            cryptedFilePath = path
            decryptedFilePath = path[:-len(ext)]
        zipfile.ZipFile(cryptedFilePath).extractall(dir, None, key)
        if remove:
            removeFile(cryptedFilePath)
        return fileToStr(decryptedFilePath)
    except Exception as e:
        if verbose:
            if logger is None:
                print(str(e))
            else:
                logger.error(str(e))
        return None

def download(url, dirPath=None, skipIfExists=False):
    """
        Based on https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py/39217788
    """
    if dirPath is None:
        dirPath = tmpDir("downloads")
    fileName = strToFilename(url.split('/')[-1])
    filePath = dirPath + "/" + fileName
    if skipIfExists and isFile(filePath):
        return filePath
    else:
        r = requests.get(url, stream=True)
        with open(filePath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        return filePath

def extract(filePath, destinationDir=None, upIfUnique=True, doDoubleExtract=True):
    if not isFile(filePath):
        print(filePath + " does not exist")
        return None
    # We get the dir of the file to extract:
    (dirPath, _, _, filenameExt) = decomposePath(filePath)
    # We extract it:
    extractedDirPath = xtract.xtract(filePath)
    # Here we check if the file end with ".tar":
    if doDoubleExtract and extractedDirPath[-4:] == ".tar":
        # So we re-extract it:
        previousPath = extractedDirPath
        extractedDirPath = xtract.xtract(extractedDirPath)
        # We remove the previous element:
        if isDir(previousPath):
            removeDirSecure(previousPath, slashCount=4)
        elif isFile(previousPath):
            removeIfExistsSecure(previousPath, slashCount=4)
    # If there is only one folder or file under extractedDirPath, we up it:
    if upIfUnique and len(sortedGlob(extractedDirPath + "/*")) == 1:
        # We get the element path:
        elementPath = sortedGlob(extractedDirPath + "/*")[0]
        # We make the dst path:
        dst = dirPath + "/" + elementPath.split("/")[-1]
        # First we check if the element exists inthe parent dir:
        if isFile(dst) or isDir(dst):
            dst += time.strftime("-%Y.%m.%d-%H.%M.%S")
        # then we move it:
        shutil.move(elementPath, dst)
        # And finally we remove the dir:
        removeDirSecure(extractedDirPath, slashCount=4)
        # We update extractedDirPath:
        extractedDirPath = dst
    # We move the element:
    if destinationDir is not None:
        # We move it:
        newDestFilePath = destinationDir + "/" + decomposePath(extractedDirPath)[3]
        shutil.move(extractedDirPath, newDestFilePath)
        # We update extractedDirPath:
        extractedDirPath = newDestFilePath
    # Finally we return the new path:
    return extractedDirPath


if __name__ == '__main__':
    # print(download("http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"))
    # extract("/home/hayj/tmp/downloads/aclImdb_v1.tar.gz")
    print(extract("/home/hayj/tmp/downloads/aclImdb_v1.tar.gz", tmpDir("aaa")))
#     normalizeNumericalFilePaths("/home/hayj/test/test1/*.txt")
#     normalizeNumericalFilePaths("/users/modhel/hayj/NoSave/Data/TwitterArchiveOrg/Converted/*.bz2")
#     strToTmpFile("hoho", subDir="test", ext="txt")
#     strToFile("haha", tmpDir(subDir="test") + "/test.txt")

#     key = 'AAA'
#     text = "bbb"
#     print(encryptFile(homeDir() + '/tmp/titi.txt', key, text=text))
#
#
#     text = decryptFile(homeDir() + '/tmp/titi.txt', key)
#
#     print(text)

    pass






