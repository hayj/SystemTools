from systemtools.logger import *
from systemtools.printer import *

def test3():
	class aaa:
		def __init__(self, logger=None, verbose=True):
			self.logger = logger
			self.verbose = verbose
		def bbb(self):
			bp([1, 2, 3], 3, self)
			bp([1, 2, 3], self, 3)
			bp([1, 2, 3], self.logger, 3, verbose=self.verbose)
			bp([1, 2, 3], 3, self.logger, verbose=self.verbose)
	logger = Logger()
	a = aaa(logger=logger, verbose=True)
	a.bbb()


if __name__ == '__main__':
	test3()
