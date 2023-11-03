
# SystemTools

This project gathers some useful Python functions and classes. We organized them in different modules:

 * **systemtools.printer**
 * **systemtools.duration**
 * **systemtools.logger**
 * **systemtools.location**
 * **systemtools.basics**
 * **systemtools.number**
 * **systemtools.file**
 * **systemtools.system**

To install all:

	pip install systools


Optionnal requirement:

	github.com/Pithikos/winlaunch.git

## systemtools.printer

This module provide function that beautiful print variables.

	>>> from systemtools.printer import *
	>>> bp(['Some text lorem ipsum dolor sit amet', {'a': 'This is some text that is short.', 'b': 'This is a longer text lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet.'}, 'Here an other text', 8, 9, [2, 3, 4, 5], 10, {1, 2, 3}])
	[
	  Some text lorem ipsum dolor sit amet,
	  {
	    a: This is some text that is short.,
	    b: This is a longer text lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit am
	  },
	  ...,
	  10,
	  { 1, 2, 3 }
	]

Use the level as second argument (from 0 to 5) to set the verbosity of the print.

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

### ProgressBar

A light alternative to [tqdm](https://github.com/tqdm/tqdm). Just wrap your iterables with the `pb` funct:

```python
for i in pb(range(iterationAmount)):
    time.sleep(0.01)
```

This will display:

	  0% [                    ]
	 20% [====                ] (1.6s left)
	 40% [========            ] (1.214s left)
	 60% [============        ] (0.813s left)
	 80% [================    ] (0.404s left)
	100% [====================] (total duration: 2.03s, mean duration: 0.01s)

By default, `pb` will **not** display more than 10 messages to do not display too much progress informations in the case you used the `nohup` command, or used a `Logger` for example.

`pb` take same parameters as the `ProgressBar` class init parameters. You can use the class directly to handle your progress bar by hand giving an iteration amount and by calling the `tic()` method at each iteration:

```python
iterationAmount = 200
pb = ProgressBar(iterationAmount)
for i in range(iterationAmount):
    time.sleep(0.01)
    pb.tic(i) # Give a message to the `tic` method to display informations about the current iteration
```

If you work on a terminal, it will automatically display informations more frenquently and replace the current line.

Init parameters are ([see the code for more information](https://github.com/hayj/SystemTools/blob/master/systemtools/duration.py#L179)):

 * **message**: will display this message at each `tic()`
 * **printRatio**: display a message at each `printRatio * iterationAmount` times you call `tic()`. Default is 0.1, meaning it will display 10%, 20%...

`tic()` parameters are:

 * **extraMessage**: use this message if you want to display informations about the current iteration. 

*Tested in Python 3 on Ubuntu.*

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

You can set the default tmp directory:

```python
from systemtools import config as systConf
systConf.defaultTmpDir = "/your/tmp/directory"
```

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
 * **floatAsReadable**: Convert a float to a readable string without "e-X".
 * **sortByKey(d)**: Sort a dict by the key. Return an `OrderedDict`.
 * **sortBy(l, desc=False, index=1)**: Sort a list of tuple (or an itemized dict) by the specific index given in parameters.
 * **chunks(l, n)**: return a list of lists (of len n) from `l`. You can also use `chunksYielder`.
 * **split(l, n)**: split a list in n parts.
 * **splitMaxSized(l, batchMaxSize)**: Split a list in multiple parts in such a way that each part has a max size of batchMaxSize.
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
 * **getDictSubElement(theDict, keys)**: This function browse the dict as a tree and return the value in the path defined by keys which is a list of dict keys. It return None if it doesn't find anything. Example: `getDictSubElement({'a': {'b': 1}}, ['a', 'b'])` return `1`.
 * **objectAsKey(o)**: Convert any object to a key, if if instead call `str(o)` or `repr(o)`, the string can change  over executions of your script due to the unordered nature of dictionnaries and sets.
 * **reducedLTS(o, amount=25)**: Same as `lts(o)` but keep only `amount` elements at the head and the tail of the object if it is a list.
 * **reduceBlank(text, keepNewLines=False) (aslias stripAll, trimAll)**: Strip a string and reduce all blank space to a unique space. If you set keepNewLines as True, it will keep a unique '\n' at each blank space which contains a '\n' or a '\r'.
 * **linearScore(x, x1=0.0, x2=1.0, y1=0.0, y2=1.0, stayBetween0And1=True)**: Give you a score f(x) defined by the linear function line (x1, y1) (x2, y2).
 * **camelCaseToUnderscoreCase(name)**: Convert a string which is formatted as the camelCase norm to the underscore_case norm.
 * **camelCaseToUnderscoreCaseDict(theDict)**: Turn each key of the dict according to `camelCaseToUnderscoreCase`.
 * **tuplesToDict(tupleList)**: Convert a list of tuples to a dict in such a way that the first element of each tuple will be the key.
 * **findDuplicates(texts, strip=True)**: Return a list a duplicates (indexes of texts in th list).
 * **intByteSize(n)**: Return the size of an integer in bytes.

## systemtools.number

This module gathers some useful basics functions on number parsing.

	>>> from systemtools.number import *

 * **parseNumber(text)**: Return the first number in the given text for any locale.
 * **getAllNumbers(text, removeCommas=False)**: Return all numbers in a string. You can also use `getFirstNumber`.
 * **getFirstNumber(text)**: Get the first numbers of a string.
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

