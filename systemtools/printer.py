
# pew in st-venv python ~/Workspace/Python/Utils/SystemTools/systemtools/printer.py

import sys
from enum import Enum
from systemtools.logger import *
from systemtools.number import truncateFloat
from collections import OrderedDict
import re
import numpy as np


class COLOR:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   end = '\033[0m'


BTYPE = Enum("BTYPE", "dict list set string type none maxdepth number object tuple ndarray")


def __bold(s):
	"""
		This function return a string wrapped with bold tokens if and only if the script is run under tty or notebook:
	"""
	# isNotebook = '__file__' not in locals()
	isTTY = sys.stdin.isatty()
	if isTTY:
		return COLOR.bold + s + COLOR.end
	else:
		return s

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


def bp(obj, level='auto', logger=None, verbose=True, **kwargs):
	try:
		if not (isinstance(level, str) or isinstance(level, int)):
			if logger is None:
				level, logger = "auto", level
			elif isinstance(logger, str) or isinstance(logger, int):
				level, logger = logger, level
			else:
				raise Exception("You must give level as an int or str and logger as a logger or as an object which has logger in its attributes")
		text = b(obj, level=level, logger=logger, verbose=verbose, **kwargs)
		log(text, logger, verbose=verbose)
	except Exception as e1:
		logException(e1, logger, location="bp", verbose=verbose)

def b(obj, level='auto', logger=None, verbose=True, **kwargs):
	"""
		levels:
		 * 0 --> only schema, very minimized...
		 * 1 --> only schema
		 * 2 --> very minimized
		 * 3 --> minimized
		 * 4 --> few minimized
		 * 5 --> full
		 * auto --> choose automatically params on-the-fly (~ level 2)
	"""
	try:
		if isinstance(level, int) and level < 0:
			level = 0
		if isinstance(level, int) and level > 5:
			level = 5
		if level == 'auto':
			level = 2
		if level <= 1:
			if "schemaOnly" not in kwargs:
				kwargs["schemaOnly"] = True
		if level <= 2:
			if "maxDictLen" not in kwargs:
				kwargs["maxDictLen"] = 10
			if "maxStringLen" not in kwargs:
				kwargs["maxStringLen"] = 100
			if "maxIterableLen" not in kwargs:
				kwargs["maxIterableLen"] = 4
			if "maxDecimals" not in kwargs:
				kwargs["maxDecimals"] = 2
		if level <= 3:
			if "maxDictLen" not in kwargs:
				kwargs["maxDictLen"] = 15
			if "addQuotes" not in kwargs:
				kwargs["addQuotes"] = False
			if "doReduceBlank" not in kwargs:
				kwargs["doReduceBlank"] = True
			if "maxStringLen" not in kwargs:
				kwargs["maxStringLen"] = 150
			if "maxIterableLen" not in kwargs:
				kwargs["maxIterableLen"] = 10
			if "maxDecimals" not in kwargs:
				kwargs["maxDecimals"] = 4
		if level <= 4:
			if "maxStringLen" not in kwargs:
				kwargs["maxStringLen"] = 400
			if "maxIterableLen" not in kwargs:
				kwargs["maxIterableLen"] = 20
			if "maxDictLen" not in kwargs:
				kwargs["maxDictLen"] = 20
		text = beautif(obj, **kwargs)
		if text.startswith("\n"):
			text = text[1:]
		return text
	except Exception as e:
		logException(e, location="b", logger=logger, verbose=verbose)




def beautif(*args, tab="  ", **kwargs):
	(values, btype) = __beautif(*args, tab=tab, **kwargs)
	return innerMultilines(values, btype, tab, "")

def __beautif\
(
	obj,
	tab="  ",
	depth=0,
	width=None,
	maxStringLen=None,
	maxIterableLen=None,
	maxDictLen=None,
	schemaOnly=False,
	addQuotes=True,
	doReduceBlank=False,
	maxDepth=None,
	doSort=True, # on sets and dicts
	maxDecimals=None,
	# TODO unknownObjectsToType=False, # type or __repr__ or __str__
	# TODO autoDetokenize=False,
):
	# try:
		# Not yet implemented
		try:
			assert width is None
			assert not schemaOnly
		except:
			raise Exception("Not yet implemented")
		# We construct recursive kwargs:
		recKwargs = locals()
		del recKwargs["obj"]
		recKwargs["depth"] += 1
		# We construct the tabulation:
		shift = tab * depth # if depth > 0 else ""
		# We calculate the reamining space:
		if width is None:
			remainingSpace = None
		else:
			remainingSpace = width - len(shift)
		# Now if test the obj type:
		if depth == maxDepth:
			return (["<max depth>"], BTYPE.maxdepth)
		elif obj is None:
			return ([str(obj)], BTYPE.none)
		elif isinstance(obj, str):
			if schemaOnly:
				return ([type(obj)], BTYPE.none)
			if doReduceBlank:
				obj = reduceBlank(obj, keepNewLines=True)
			if maxStringLen is not None:
				obj = obj[:maxStringLen]
			# if remainingSpace is not None and len(obj) >= remainingSpace:
			# 	objList = [""]
			# 	objListIndex = 0
			# 	for i in range(len(obj)):
			# 		if len(objList[objListIndex]) >= remainingSpace:
			# 			objList.append("")
			# 			objListIndex += 1
			# 		objList[objListIndex] += obj[i]
			# 	newObj = ""
			# 	for current in objList:
			# 		newObj += shift + current + "\n"
			# 	obj = newObj[:-1]
			return ([obj], BTYPE.string)
		elif isinstance(obj, dict) or isinstance(obj, OrderedDict):
			if isinstance(obj, OrderedDict):
				obj = dict(obj)
			result = []
			result.append("{")
			quote = "'" if addQuotes else ""
			if doSort:
				keys = sorted(list(obj.keys()), key=str)
			else:
				keys = obj.keys()
			if maxDictLen is not None and len(keys) > maxDictLen:
				amount = int(maxDictLen / 2)
				if amount == 0:
					amount = 1
				keysParts = [keys[:amount], keys[-amount:]]
			else:
				keysParts = [keys]
			for keysPartsIndex in range(len(keysParts)):
				keysPart = keysParts[keysPartsIndex]
				for key in keysPart:
					value = obj[key]
					(values, btype) = __beautif(value, **recKwargs)
					values = innerMultilines(values, btype, tab, shift + tab)
					result.append(quote + __bold(str(key)) + quote + ": " + values + ",")
				if len(keysParts) > 1 and keysPartsIndex != len(keysParts) - 1:
					result.append("...,")
			# We remove the comma:
			try:
				if result[-1][-1] == ",":
					result[-1] = result[-1][:-1]
			except: pass
			# We close the dict:
			result.append('}')
			return (result, BTYPE.dict)
		elif isinstance(obj, list) or isinstance(obj, set) or isinstance(obj, tuple):
			isSet = isinstance(obj, set)
			isTuple = isinstance(obj, tuple)
			isList = isinstance(obj, list)
			if isSet and doSort:
				obj = sorted(obj, key=str)
			parts = [obj]
			if maxIterableLen is not None and len(obj) > maxIterableLen:
				amount = int(maxIterableLen / 2)
				if amount == 0:
					amount = 1
				parts = [obj[:amount], obj[-amount:]]
			result = []
			if isSet:
				result.append("{")
			elif isTuple:
				result.append("(")
			else:
				result.append("[")
			partIndex = 0
			for partIndex in range(len(parts)):
				part = parts[partIndex]
				for value in part:
					(values, btype) = __beautif(value, **recKwargs)
					values = innerMultilines(values, btype, tab, shift + tab)
					result.append(values + ",")
				if len(parts) > 1 and partIndex != len(parts) - 1:
					result.append("...,")
			# We remove the comma:
			try:
				if result[-1][-1] == ",":
					result[-1] = result[-1][:-1]
			except: pass
			# We close the iterable:
			if isSet:
				result.append("}")
				return (result, BTYPE.set)
			elif isTuple:
				result.append(")")
				return (result, BTYPE.tuple)
			else:
				result.append("]")
				return (result, BTYPE.list)
		elif isinstance(obj, int) or isinstance(obj, float):
			if isinstance(obj, float) and maxDecimals is not None:
				obj = truncateFloat(obj, maxDecimals)
			return ([str(obj)], BTYPE.number)
		elif isinstance(obj, bool):
			return ([str(obj)], BTYPE.boolean)
		elif isinstance(obj, np.ndarray):
			return (str(obj).split("\n"), BTYPE.ndarray)
		else:
			text = str(obj)
			if doReduceBlank:
				text = reduceBlank(text, keepNewLines=True)
			if maxStringLen is not None and len(text) > maxStringLen:
				return ([text[:maxStringLen] + "..."], BTYPE.object)
			else:
				return ([text], BTYPE.object)

			
	# except Exception as e:
	# 	print(e)

def innerMultilines(values, btype, tab, shift):
	if values is None or len(values) == 0:
		return ""
	elif len(values) == 1:
		return values[0]
	else:
		hasOnlyLittleElements = True
		for current in values:
			if len(current) > 50:
				hasOnlyLittleElements = False
				break
		if hasOnlyLittleElements and not btype == BTYPE.ndarray:
			result = " ".join(values)
			return result
		else:
			# if values[0][0] == "\n":
			# 	values[0] = values[1:]
			result = ""
			if len(values[0]) == 1:
				result += "\n" + shift + values[0] + "\n"
			else:
				result += values[0] + "\n"
			doMiddleTab = btype in [BTYPE.list, BTYPE.dict, BTYPE.set, BTYPE.tuple]
			if doMiddleTab:
				for i in range(1, len(values) - 1):
					values[i] = tab + values[i]
			for i in range(1, len(values)):
				current = values[i]
				result += shift + current + "\n"
			result = result[:-1]
			result = result.replace("\n" + shift + tab + "\n", "\n") # TODO find a clean way to handle this
			return result


def test1():
	obj = \
	{
		'uuu': [1, 2, 3, 4, 5, 6, {"y", "r", "e", "o", "p", "q"}, [5] * 100],
		'eee': "blah " * 200,
		'aaa': "bleh " * 400,
		'ccc': "bluh " * 4,
		'ddd': {"u": "e", "i": {"u": "e", "i": "e", "i": {"u": "e " * 4, "i": "e " * 4}}},
	}
	print(beautif(obj, maxIterableLen=5, maxDictLen=5, maxStringLen=100))

def test2():
	from datatools.jsonutils import NDJson
	row = None
	for row in NDJson("/home/hayj/tmp/mbti-datasets/mbti-dataset-2019.06.21-20.54/0.ndjson.bz2"):
		break
	bp(row, maxDepth=3)




if __name__ == '__main__':
	test3()