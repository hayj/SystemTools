import enum
from enum import Enum



def e(a, b=None, raiseException=False, logger=None):
	errorText1 = "Please give at least an enum.EnumMeta or an Enum"
	errorText2 = "Please give at least an enum.EnumMeta"
	if a is None:
		raise Exception(errorText1)
	if b is None:
		if isinstance(a, enum.EnumMeta):
			return [x.name for x in a]
		elif isinstance(a, Enum):
			return a.name
		else:
			if raiseException:
				raise Exception(errorText)
			else:
				if logger is not None:
					logger.error(errorText1)
				return a
	else:
		theEnumMeta = None
		theValue = None
		if isinstance(a, enum.EnumMeta):
			theEnumMeta = a
			theValue = b
		elif isinstance(b, enum.EnumMeta):
			theEnumMeta = b
			theValue = a
		else:
			if raiseException:
				raise Exception(errorText2)
			else:
				if logger is not None:
					logger.error(errorText2)
				return theValue
		theValue = enumCast(theValue, theEnumMeta, raiseException=raiseException)
		if not isinstance(theValue, Enum):
			errorText3 = "Cannot convert " + str(theValue) + " to an Enum"
			if raiseException:
				raise Exception(errorText3)
			else:
				if logger is not None:
					logger.error(errorText3)
				return theValue
		return theValue


def enumCast(text, theEnum, logger=None, verbose=True, raiseException=False):
	try:
		if isinstance(text, Enum):
			return text
		elif isinstance(text, int):
			return list(theEnum)[text - 1]
		else:
			return theEnum[text]
	except Exception as e:
		errorText1 = "Cannot find " + str(text) + " in " + str(theEnum)
		if raiseException:
			raise Exception(errorText1)
		else:
			if logger is not None:
				logger.error(errorText1)
			return None

def enumEquals(a, b):
	if isinstance(a, str) or isinstance(b, str):
		if isinstance(a, Enum):
			a = a.name
		if isinstance(b, Enum):
			b = b.name
	return a == b





if __name__ == '__main__':
	DATASET = Enum("DATASET", "year2015 year2016")


	print(e(DATASET))
	print()
	print(e(DATASET.year2015))
	print(e(DATASET.year2016))
	print()
	print(e("year2015", DATASET))
	print(e("year2016", DATASET))
	print()
	print(e(DATASET.year2015, DATASET))
	print(e(DATASET.year2016, DATASET))
	print()
	print(e(DATASET.year2015.value, DATASET))
	print(e(DATASET.year2016.value, DATASET))
