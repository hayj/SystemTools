
from enum import Enum
from systemtools.location import *
from systemtools.basics import *
from systemtools.system import *
import json




# MONGO_SERVERS = Enum("MONGO_SERVERS", "localhost datascience01 hjlat jamy tipi")
# def getMongoAuth(user="hayj", mongoServer=MONGO_SERVERS.localhost, passwordsPath=None):
def getMongoAuth(user=None, hostname="localhost", passwordsPath=homeDir() + "/.ssh/mongo-passwords.json"):
    """
        (user, password, host) = getMongoAuth()
        passwords are stored in ~/.ssh/mongo-passwords.json
    """
    def jsonFileToObject(path):
        with open(path) as data:
            data = jsonToObject(data)
        return data
    def jsonToObject(text):
        return json.load(text)
    host = "localhost"
#     if mongoServer == "datascience01" and not isHostname("datascience01"):
    if hostname == "datascience01" and not isHostname(hostname):
        host = "ds01.dc01.octopeek.com" # 212.129.44.40
    passwords = jsonFileToObject(passwordsPath)
    password = None
    if user is not None:
        password = passwords[user]
    return (user, password, host)

def getOctodsMongoAuth(*args, **kwargs):
    return getDatascience01MongoAuth(*args, **kwargs)
def getDatascience01MongoAuth(*args, **kwargs):
    return getMongoAuth(*args, user="hayj", hostname="datascience01", **kwargs)
def getStudentMongoAuth(*args, **kwargs):
    return getMongoAuth(*args, user="student", hostname="datascience01", **kwargs)

# def homeDir(user=None, homePaths=["/users/modhel", "/home"]):
#     if user is None:
#         user = getpass.getuser()
# #         if user in ["root", "admin", "superuser", "mongo", "mongod", "pydev"]:
# #             user = defaultUser
#     for currentHomePath in homePaths:
#         currentPath = currentHomePath + "/" + user
#         if isDir(currentPath):
#             return currentPath
#     return None

# def dataPath(dirname="Data", startDirs=["/users/modhel-nosave/hayj", "/home/hayj"], subDirSamples=["Similarity", "TwitterArchiveOrg"]):
#     walkParams = {"followlinks": True, "topdown": False}
#     pathSamples = []
#     for current in subDirSamples:
#         pathSamples.append(dirname + "/" + current)
#     for startDir in startDirs:
#         for root, dirs, files in os.walk(startDir, topdown=False):
#             for name in dirs:
#                 thePath = os.path.join(root, name)
#                 for sample in pathSamples:
#                     if re.match("^.*" + sample + "$", thePath) is not None:
#                         return "/".join(thePath.split("/")[0:-1])
#     return None


