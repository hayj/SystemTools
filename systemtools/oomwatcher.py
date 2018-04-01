# coding: utf-8


########## WORSPACE IN PYTHON PATH ##########
# Include all Paths :
# TODO faire un include de tous les sous dossiers du Workspace en remontant 4 dossiers
# TODO (mettre une variable pour le nombre de dossier a remonter).
# TODO mettre aussi le changement en utf-8
# TODO Et mettre le os.chdir("??") aussi
# TODO Faire une sorte d'entete pour chaque fichier python
# Updated 09/03/17
workspaceName = "SystemTools" # Set the name of the Workspace in all ancestors folders
onlyInit = False # TODO
import sys
import os
import re
def dirsHasRegex(dirs, regex):
    if not isinstance(dirs, list):
        dirs = [dirs]
    # for all subdirs:
    for currentDir in dirs:
        # We get all files:
        files = getFileNames(currentDir)
        # We check if there .py or __init__.py:
        for fname in files:
            if re.search(regex, fname) is not None:
                return True
    return False

def getFileNames(currentFolder):
    files = [item for item in os.listdir(currentFolder) if os.path.isfile(os.path.join(currentFolder, item))]
    return files

def getSubdirsPaths(currentFolder):
    dirs = [currentFolder + item + "/" for item in os.listdir(currentFolder) if os.path.isdir(os.path.join(currentFolder, item))]
    return dirs

# We get the Workspace dir:
currentFolder = os.path.dirname(os.path.abspath(__file__))
workspace = currentFolder.split(workspaceName)[0] + workspaceName + "/"
# And while there are folders to watch:
penddingFolderList = [workspace]
pathsToAdd = []
while len(penddingFolderList) != 0:
    # We pop the current folder in in the pending queue:
    currentFolder = penddingFolderList.pop(0)
    if not currentFolder.split("/")[-2].startswith("."):
        hasPy = dirsHasRegex(currentFolder, ".py$")
        atLeastOneSubDirHasInit = dirsHasRegex(getSubdirsPaths(currentFolder), "__init__.py")
        # We add it in the path list:
        if hasPy or atLeastOneSubDirHasInit:
            pathsToAdd.append(currentFolder)
        # And We add the subfolders in the pending queue if there is no __init__.py:
        if not atLeastOneSubDirHasInit:
            subDirs = getSubdirsPaths(currentFolder)
            penddingFolderList += subDirs
# We add all paths in the python path:
print(pathsToAdd)
for path in pathsToAdd:
    sys.path.append(path)
#     print path
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################




# nn pew in systemtools-venv python /home/hayj/wm-dist-tmp/SystemTools/systemtools/oomwatcher.py "/home/hayj/taonews-logs/kill-taonews.sh" -t 90 -v
# pew in systemtools-venv python /home/hayj/wm-dist-tmp/SystemTools/systemtools/oomwatcher.py "/home/hayj/oomwatcher-logs/test.sh" -t 5 -v

import argparse
from systemtools.basics import *
from systemtools.logger import *
from systemtools.duration import *
from systemtools.system import *
import time
import sh
from systemtools.logger import log, logInfo, logWarning, logError, Logger


def getArgs():
    # Get args:"
    parser = argparse.ArgumentParser()
    parser.add_argument('scriptPath', help='The script you want to exec')
    parser.add_argument("-v", "--verbose", help="Display infos", action="store_true")
    parser.add_argument("-t", "--threshold", help="The % of memory you want to trigger the script execution")
    parser.add_argument("-s", "--sleep", help="The time interval between each memory check")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = getArgs()
    scriptPath = args.scriptPath
    threshold = 90
    try:
        threshold = int(args.threshold)
        assert threshold > 0
        assert threshold < 1.0
    except: pass
    verbose = False
    try:
        verbose = args.verbose
        assert isinstance(verbose, bool)
    except: pass
    sleepInterval = 10
    try:
        sleepInterval = args.sleep
        assert sleepInterval > 0
        assert sleepInterval < 10000
    except: pass
    
    logger = Logger("oomwatcher.log")
    
    while True:
        time.sleep(10.0)
        if getRandomFloat() > 0.95:
            logInfo("getMemoryPercent() = " + str(getMemoryPercent()), logger=logger)
            logInfo("threshold = " + str(threshold), logger=logger)
        if getMemoryPercent() > threshold:
            try:
                sh.bash(scriptPath) # sh.bash("/home/hayj/taonews-logs/kill-taonews.sh")
                logInfo("Script executed", logger=logger)
            except Exception as e:
                logError(str(e), logger=logger)
                
        
