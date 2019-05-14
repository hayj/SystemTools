# pew in st-venv python ~/Workspace/Python/Utils/SystemTools/systemtools/test/sys-test.py

import re
import socket

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
