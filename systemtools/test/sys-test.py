# pew in st-venv python ~/Workspace/Python/Utils/SystemTools/systemtools/test/sys-test.py

import re
import socket


from systemtools.system import *



def test1():
	def isHostname(hostname):
		return getHostname().startswith(hostname)
	def getHostname():
		return socket.gethostname()
	def getTipiNumber():
		try:
			return int(re.search("[0-9]+", getHostname()).group(0))
		except:
			return None

	tipiNumber = getTipiNumber()
	if tipiNumber is None:
		print("Test...")
	elif tipiNumber < 8:
		print("Task 1...")
	else:
		print("Task 2...")


def test2():
	for i in range(1000):
		bash("killbill phantomjs")



if __name__ == '__main__':
	test2()