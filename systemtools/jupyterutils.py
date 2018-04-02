import sys

def getIpynbArgv(jupyterClue="ipykernel_launcher.py"):
    if len(sys.argv) == 0:
        return []
    if jupyterClue in sys.argv[0]:
        return []
    return sys.argv[2:]