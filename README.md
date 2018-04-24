
# SystemTools

This project gathers some useful Python functions and class. We organized them in different modules:

 * **systemtools.duration**
 * **systemtools.logger**
 * **systemtools.location**
 * **systemtools.basics**
 * **systemtools.number**
 * **systemtools.file**
 * **systemtools.system**

To install all:

	pip install hjsystemtools

## systemtools.duration

This module provide some useful class to handle time.

	>>> from systemtools.duration import *

### TicToc

This class allow an easy print of computation time in your scripts:

	>>> tt = TicToc()
	>>> tt.tic() # Start the timer
	>>> <do something...>
	>>> tt.tic() # Print the time duration (human readable) since the previous tic()
	tic: 1s
	>>> <do something...>
	>>> tt.tic()
	tic: 1s
	>>> tt.toc() # Print the total duration
	toc total duration: 2s

You can give `msg` parameter to add a message to the printed duration. You can also choose to do not display anything using `display=False`.

Both `tic` and `toc` methods return the time spent in seconds.

### Timer

This class call a function each n seconds:

	>>> timer = Timer(myFunct, 5)
	>>> timer.start()

You can stop it using:

	>>> timer.stop()

Set `sleepFirst=True` if you don't want to call your funct at the startup of the timer.

## systemtools.logger

A Logger class is a wrapper over `logging`.

	>>> from systemtools.logger import *
	>>> logger = Logger("test.log") # Give a file path
	>>> logger.info("a") # Print infos
	>>> logger.error("b") # Print errors...

If you created a class which contains `logger` and `verbose` like this one:

	>>> class LoggerTest:
	...     def __init__(self, logger=None, verbose=True):
	...             self.logger = logger
	...             self.verbose = verbose

And use functions `log`, `logError`... this way in a method of your class:

	...             log("Initialized....", self)

So the log function will automaticllay check if verbose is True, and if there is no `logger`, it will simply print your message.

You can also use `logException` this way:

	...             logException(e, self) # You can give message (string) and location (string) parameters

You can also give a `Logger` instead of a class instance:

	>>> log("a", logger)
	>>> logException(e, logger, verbose=myVerbose)
	>>> ...

## systemtools.location

This module gathers some useful functions on file system location.

	>>> from systemtools.location import *

 * **sortedGlob(regex, caseSensitive=True, sortBy=GlobSortEnum.NAME, reverse=False)**: This function works the same as glob.glob but return an ordered list of files path. glob.glob return (by default) a ordered list which can change across OS or executions and it is prone to errors in your python script. You can use different orders via sortBy: GlobSortEnum.<MTIME|NAME|SIZE|NUMERICAL_NAME> the last one is the same as name but take into account numbers (e.g. test1.txt < test10.txt).
 * **homeDir()** : Return the path of your home dir.
 * **tmpDir(_file_=None, subDir=None)**: Return the path of the tmp dir, If you give `__file__` in first param, the tmp dir will be "tmp" in the current directory, else it will be ~/tmp. You can set `subDir` in parameters.
 * **execDir(_file_=None)**: Get the current directory, it is better to give `__file__` in parameter to be sure to get the dir of the current Python script.
 * **isDir(path)**: Return True is the given path is a directory.
 * **isFile(path)**: Return True is the given path is a file.
 * **decomposePath(path)**: Return a tuple (dir, filename, ext, filenameAndExt) of a path.

## systemtools.basics

This module gathers some useful basics functions.

	>>> from systemtools.basics import *

* **listSubstract(a, b)**: Substract all `b` items from `a`.
* **convertDate(readableDate=None, dateFormat=DATE_FORMAT.datetime)**: Convert a readable date (wrote by a human) in a date format you chose. Warning : utc shift may appear. DATE_FORMAT enum contains "datetimeString datetime timestamp arrow arrowString humanize".
 * **mergeDicts(dict1, ...)**: shallow copy of all dict and merge into a new dict
 * **reduceDictStr**: See the code for parameters. Reduce all strings of a dict in order to print it.
 * **stripAccents(text)**: Remove all accents of a string.
 * **printLTS(l)**: Pretty print a list or a dict. Use `listToStr` internally.
 * **listToStr(l)**: Convert a list or a dict to a pretty string.
 * **floatAsReadable**: Convert a float to a readble string without "e-X".
 * **sortByKey(d)**: Sort a dict by the key. Return an `OrderedDict`.
 * **sortBy(l, desc=False, index=1)**: Sort a list of tuple (or an itemized dict) by the specific index given in parameters.
 * **chunks(l, n)**: return a list of list (of len n) from `l`. You can also use `chunksYielder`.
 * **split(l, n)**: split a list in n parts.
 * **normalize(l)**: Normalize (between 0.0 and 1.0) all elements of a list according to the sum of all elements.
 * **getRandomInt(a=None, b=None, seed=None, count=1)**: Return a random int between `a` and `b`.
 * **getRandomFloat(min=0.0, max=1.0, decimalMax=2)**: Return a random float between `min` and `max`.
 * **getRandomStr(digitCount=10, withTimestamp=True)**: Return a random string with a timestamp if enabled.
 * **getRandomName(addInt=True, maxInt=100)**: Return a random name with a random int.
 * **Random class**: This class is useful when you want to seed random values and reset it after the class usage. See the code for more informations.
 * **dictContains(d, key)**: Equivalent to `key in d and d[key] is not None`.
 * **intersection(lists)**: Return the intersection of all lists.
 * **reduceStr**: Reduce a str, you can set booleans removeNumbers, toLowerCase, removeAccents and removePunct.
 * **varname(p)**: Return the name of p from the Python script.
 * **stripAllLines(text, removeBlank=True)**: Return the text but strip all lines.
 * **byteToStr(b)**: Convert bytes to str.

## systemtools.number

This module gathers some useful basics functions on number parsing.

	>>> from systemtools.number import *

 * **parseNumber(text)**: Parse the first number in the given text for any locale.
 * **getAllNumbers(text, removeCommas=False)**: Return all numbers in a string. You can also use `getFirstNumber`.
 * **getFirstNumber(text, *args, **kwargs)**: Get the first numbers of a string.
 * **removeAllNumbers(text)**: Remove all numbers from a string.
 * **truncateFloat(f, n)**: Truncates/pads a float f to n decimal places without rounding.

## systemtools.file

This module gathers some useful functions on file and directories management.

	>>> from systemtools.file import *

* **getLastModifiedTimeSpent(path, timeSpentUnit=TIMESPENT_UNIT.HOURS)**: Return the time spent after the last modified event on a path (file or directory).
* **strToFilename(text)**: Convert a string in a filename (storable on the disk). So it will remove all non permitted chars.
* **mkdir(path)**: Create a directory if it doesn't already exist.
* **globRemove(globPattern)**: Remove file according to a glob pattern similar to the glob lib.
* **removeFile(path)**: Remove a file or a list of files.
* **fileToStr(path)**: Load a file and return the string in.
* **fileToStrList**: Load a file and return a list of strings. You can set `strip` as `False` to don't strip all lines, `skipBlank` as `False` to keep blank lines, you can choose your comment start indicator using `commentStart` (default is "###").
* **strToFile(text, path)**: Store a string in a file.
* **strToTmpFile(text, name=None, ext="", addRandomStr=False)**: Store a string to a tmp file (using `tmpDir` function). Example: strToTmpFile("a", "test.txt").
* **strListToTmpFile**: Use `strToTmpFile` but for a list of strings which is concatened.
* **normalizeNumericalFilePaths(globRegex)**: This function get a glob path and rename all "file1.json", "file2.json"... "file20.json" to "file01.json", "file02.json"... "file20.json" to better sort the folder by file names.
* **encryptFile(path, key, text=None, remove=True)**: This function encrypt a file, if you give text in `text` parameter, the function will create the file. Return True if all is ok. You need to install 7zip using `sudo apt-get install p7zip-full` on Linux. Set remove as `False` if you don't want to remove the decrypted file.
* **decryptFile(path, key, remove=True)**: This function decrypt a file and return the text. Set remove as `False` if you don't want to remove the encrypted file.

## systemtools.system

This module gathers some useful functions on the OS management.

	>>> from systemtools.system import *

 * **getUsedPorts()**: Return all busy ports on your machine (works on Linux using netstat).
 * **getUser()**: Equivalent to `getpass.getuser()`
 * **setCallTimeout(timeout) and resetCallTimeout()**: Use `setCallTimeout` to set a timeout before calling a function (so you can catch an Exception if the function is too long), then reset the timeout.
 * **getRAMTotal()**: Return the amount of RAM in Go
 * **cpuCount()**: Equivalent to `multiprocessing.cpu_count()`
 * **isHostname(h)**: Return `True` if the hostname of the current computer starts with `h`.
 * **getHostname()**: Equivalent to `socket.gethostname()`
 * **randomSleep(min=0.1, max=None)**: Sleep between min and max. If max is None: max = min + 0.2 * min.
 * **getMemoryPercent()**: Return the % of memory usage.

