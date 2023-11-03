# pew in st-venv python ~/Workspace/Python/Utils/SystemTools/systemtools/system.py

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
import multiprocessing
import time
import signal
import getpass
from systemtools.basics import *
from systemtools.file import *
from systemtools.number import *
from psutil import virtual_memory
import traceback
import requests

def myIp(driver=None, ipUrl="https://api.ipify.org?format=json"):
    try:
        if driver is None:
            data = requests.get(ipUrl).text
        else:
            data = driver.get(ipUrl).page_source
        return re.search("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", data).group(0)
    except:
        return None

def sshStats\
(
    address,
    user=None,
    timeout=6,
    successToken='connection_success',
):
    """
        This function return stats on a server.
        https://askubuntu.com/questions/9487/whats-the-difference-between-load-average-and-cpu-load
    """
    if user is None:
        user = getUser()
    results = bash('timeout ' + str(timeout+1) + ' ssh -o BatchMode=yes -o ConnectTimeout=' + str(timeout) + ' ' + user + '@' + address + ' "echo ' + successToken + ' ; uptime ; nproc ; grep MemTotal /proc/meminfo ; grep MemAvailable /proc/meminfo"', doPrint=False)
    if successToken in results:
        results = results.split("\n")
        for i in range(len(results)):
            if "load average" in results[i]:
                break
        stats = dict()
        try:
            loadAverageLine = results[i]
            numbers = getAllNumbers(loadAverageLine)
            stats['1min_loadavg'] = numbers[-3]
            stats['5min_loadavg'] = numbers[-2]
            stats['15min_loadavg'] = numbers[-1]
        except Exception as e:
            print(e)
        try:
            stats['cpu_count'] = getFirstNumber(results[i+1])
            stats['normalized_1min_loadavg'] = truncateFloat(stats['1min_loadavg'] / stats['cpu_count'], 3)
            stats['normalized_5min_loadavg'] = truncateFloat(stats['5min_loadavg'] / stats['cpu_count'], 3)
            stats['normalized_15min_loadavg'] = truncateFloat(stats['15min_loadavg'] / stats['cpu_count'], 3)
        except Exception as e:
            print(e)
        try:
            stats['mem_total'] = truncateFloat(getFirstNumber(results[i+2]) / 1e6, 2)
        except Exception as e:
            print(e)
        try:
            stats['mem_available'] = truncateFloat(getFirstNumber(results[i+3]) / 1e6, 2)
        except Exception as e:
            print(e)
        return stats
    else:
        return None


def pipFreeze(*grep, logger=None, verbose=False):
    try:
        try:
            from pip._internal.operations import freeze
        except ImportError:  # pip < 10.0
            from pip.operations import freeze
        x = list(freeze.freeze())
        elements = set()
        for currentGrep in grep:
            print(currentGrep)
            if currentGrep is None:
                elements = elements.union(set(x))
            else:
                for p in x:
                    if currentGrep in p:
                        elements.add(p)
        if verbose:
            if logger is not None:
                logger.log(str(elements))
            else:
                print(str(elements))
        return elements
    except Exception as e:
        if verbose:
            if logger is not None:
                logger.log(str(e))
            else:
                print(str(e))            
        return None


def isPlatform(text):
    if text is None:
        return False
    text = text.lower()
    currentPlatform = platform()
    currentPlatform = currentPlatform.lower()
    return currentPlatform.startswith(text)
def windows():
    return isPlatform("windows")
def linux():
    return isPlatform("linux")
def mac():
    return isPlatform("os") or isPlatform("mac")
def platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows',
        'nt' : 'Windows',
        'win64' : 'Windows',
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]

# def sh(*args, **kwargs):
#     return exec(*args, **kwargs)
def bash(*args, **kwargs):
    return exec(*args, **kwargs)
def exec(commands, doPrint=True, useBuiltin=False, logger=None, verbose=True):
    """
        Execute any command as a bash script for Linux platforms.
        In case useBuiltin is `True`, no output will be returned.
        For Linux platforms, the function will source `~/.bash_profile`, `~/.bashrc` and `~/.bash_aliases` if they exist.
    """
    if linux():
        if isinstance(commands, list):
            commands = "\n".join(commands)
        script = ""
        if isFile(homeDir() + "/.bashrc"):
            script += "source ~/.bashrc" + "\n"
        if isFile(homeDir() + "/.hjbashrc"):
            script += "source ~/.hjbashrc" + "\n"
        if isFile(homeDir() + "/.bash_profile"):
            script += "source ~/.bash_profile" + "\n"
        if isFile(homeDir() + "/.bash_aliases"):
            script += "shopt -s expand_aliases" + "\n"
            script += "source ~/.bash_aliases" + "\n"
        script += commands
        scriptPath = strToTmpFile(script)
        result = None
        try:
            # result = subprocess.Popen(["bash", scriptPath], shell=False,
            #     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if doPrint and useBuiltin:
                os.system("bash " + scriptPath)
            else:
                # result = os.popen("bash " + scriptPath).read()
                sp = subprocess.Popen(["bash", scriptPath], shell=False,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result, error = sp.communicate()
                result = byteToStr(result)
                error = byteToStr(error)
                if error is not None:
                    result += "\n\n" + error
                result = result.strip()
            # result = sh.bash(scriptPath)
        except Exception as e:
            result = "Exception type: " + str(type(e)) + "\n"
            result += "Exception: " + str(e)
            try:
                result +=  "\n" + traceback.format_exc()
            except: pass
        rm(scriptPath)
        if doPrint and verbose and result is not None and len(result) > 0:
            if logger is None:
                print(result)
            else:
                logger.log(result)
        return result
    elif windows():
        raise Exception("Please implement exec funct for Windows platform")
    elif mac():
        raise Exception("Please implement exec funct for OS X platform")
    else:
        raise Exception("Unkown platform " + str(platform()))


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

def isUser(text):
    return getUser().startswith(text)

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

def isDocker():
    return isDir("/hosthome")

def isHostname(hostname):
    return getHostname().startswith(hostname)

def getHostname():
    return socket.gethostname()


# Deprecated (use sh lib instead):
def sleep(seconds):
    time.sleep(seconds)

# # Deprecated (use sh lib instead):
# def bash(text):
#     """
#         Deprecated: use sh lib instead
#         But it doesn't work on eclipse, use instead a python command line
#     """
#     text = text.split(" ")
#     return subprocess.call(text)

# # Deprecated (use sh lib instead):
# def bash2(text):
#     """
#         Deprecated: use sh lib instead
#         But it doesn't work on eclipse, use instead a python command line
#     """
#     os.system(text)

# # Deprecated (use sh lib instead):
# def bash3(text):
#     """
#         Deprecated: use sh lib instead
#         But it doesn't work on eclipse, use instead a python command line
#     """
# #     text = ['/bin/bash', '-c'] + text.split(" ")
#     text = text.split(" ")
#     return subprocess.check_output(text)

# # Déprecated (use sh lib instead):
# def bash4(text):
#     """
#         Deprecated: use sh lib instead
#         But it doesn't work on eclipse, use instead a python command line
#     """
# #     text = ['/bin/bash', '-c'] + text.split(" ")
#     text = text.split(" ")
#     pipe = subprocess.Popen(text, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable='/bin/bash')
#     stdout, stderr = pipe.communicate()
#     return stdout



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


# psutil.virtual_memory()["available"]

# def stout():
#     """
#     Return True if we are on stout
#     """
#     return (psutil.cpu_count(logical=True) > 40) and ((psutil.virtual_memory().total / (1*(10**9))) > 40);

def getMemoryUsage(d):
    return asizeof(d)

def freeRAM():
    """
        return the actual free ram space in Go
    """
    return truncateFloat(psutil.virtual_memory().available / (1*(10**9)), 2)

def warnFreeRAM(logger=None, verbose=True):
    if verbose:
        fr = freeRAM()
        msg = str(fr) + "g of RAM remaining."
        if logger is None:
            print(msg)
        else:
            logger.log(msg)
        if fr < 2:
            msg = "WARNING: the remaining RAM is very low!"
            if logger is None:
                print(msg)
            else:
                logger.log(msg)


def usedRAM():
    return truncateFloat(psutil.virtual_memory().used / (1*(10**9)), 2)

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

def isWorkingProxy(proxy, verbose=False):
    try:
        http_proxy  = "http://" + proxy
        https_proxy = "https://" + proxy
        ftp_proxy   = "ftp://" + proxy
        proxyDict = { 
                      "http"  : http_proxy, 
                      "https" : https_proxy, 
                      "ftp"   : ftp_proxy
                    }
        for url in \
        [
            "https://www.wikipedia.org/",
            "https://www.python.org/",
        ]:
            r = requests.get\
            (
                url,
                proxies=proxyDict,
                timeout=10,
            )
            if len(r.text) > 100:
                return True
    except Exception as e:
        if verbose:
            print(str(e) + "\n" + str(traceback.format_exc()))
    return False


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

def html2png(urlOrPath, destPath=None, width=None, height=None):
    """
        If this function doesn't word, try firefox command line.
        If there are an old firefox profile error, just do
        `rm -rf ~/.mozilla` if you are in a docker container...`
    """
    assert urlOrPath is not None
    if not urlOrPath.startswith("htt") and not urlOrPath.startswith("file"):
        urlOrPath = "file://" + urlOrPath
    if urlOrPath.startswith("file"):
        assert isFile(urlOrPath.replace("file://", ""))
    size = ""
    if width is not None:
        size = str(width)
        if height is not None:
            size += "," + str(height)
        size = "--window-size=" + size
    start = "firefox -headless -screenshot"
    if destPath is None and urlOrPath.startswith("file"):
        destPath = urlOrPath.replace("file://", "") + ".png"
    assert destPath is not None
    command = start + " " + destPath + " " + urlOrPath + " " + size
    bash(command, verbose=False)
    return destPath


def installSent2Vec():
    try:
        import sent2vec
    except:
        # from systemtools.system import bash
        bash("pip install Cython")
        bash("git clone https://github.com/epfml/sent2vec.git")
        bash("pip install ./sent2vec/")
        remove("sent2vec")
        import sent2vec



def cropPNG(path, dst=None):
    if dst is None:
        dst = path
    bash("convert " + path + " -trim " + dst + "", verbose=False)
    return dst


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


def testHtmlToPNG():
    html2png("/home/hayj/Workspace/Python/Utils/MachineLearning/machinelearning/attmap/template-test2.html")


if __name__ == "__main__":
    testHtmlToPNG()
    # print(tipiNumber())
    # print(getRAMTotal())

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


