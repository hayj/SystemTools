# coding: utf-8
# http://sametmax.com/ecrire-des-logs-en-python/

import logging
from logging.handlers import RotatingFileHandler
from systemtools.system import *
from systemtools.basics import *
from systemtools.file import *
from enum import Enum
import traceback


LOGTYPE = Enum('LOGTYPE', 'error info warning')


def logException(e=None, obj=None, message=None, location=None, logger=None, verbose=True):
    if message is None:
        message = ""
    else:
        message += "\n"
    if location is not None:
        message += "Exception location: " + location + "\n"
    if e is not None:
        message += "Exception type: " + str(type(e)) + "\n"
        message += "Exception: " + str(e)
        try:
            message +=  "\n" + traceback.format_exc()
        except: pass
    log(message, obj=obj, logger=logger, verbose=verbose, logtype=LOGTYPE.error)
def logInfo(text, obj=None, logger=None, verbose=True):
    log(text, obj=obj, logger=logger, verbose=verbose, logtype=LOGTYPE.info)
def logWarning(text, obj=None, logger=None, verbose=True):
    log(text, obj=obj, logger=logger, verbose=verbose, logtype=LOGTYPE.warning)
def logError(text, obj=None, logger=None, verbose=True):
    log(text, obj=obj, logger=logger, verbose=verbose, logtype=LOGTYPE.error)


def log(text, obj=None, logger=None, verbose=True, logtype=LOGTYPE.info):
    """
        This obj must have a logger and a verbose attr.
        Else you can give it in params.
    """
    if obj is not None and isinstance(obj, Logger):
        logger, obj = obj, None
    if obj is not None:
        try:
            obj.logger
            obj.verbose
        except NameError:
            print(text)
        else:
            if obj.verbose:
                if obj.logger is None:
                    print(text)
                else:
                    logWithLogger(text, obj.logger, logtype)
    elif verbose:
        if logger is None:
            print(text)
        else:
            logWithLogger(text, logger, logtype)

def logWithLogger(text, logger, logtype):
    if logtype == LOGTYPE.info:
        logger.info(text)
    if logtype == LOGTYPE.error:
        logger.error(text)
    if logtype == LOGTYPE.warning:
        logger.warning(text)


class Logger():
    def __init__(self, outputPath="output.log", moWeightMax=1, prefix=None, remove=False):
        self.prefix = prefix
        if self.prefix is None:
            self.prefix = ""
        self.outputPath = outputPath
        self.moWeightMax = moWeightMax
        self.randomName = getRandomStr()
        # Now we remove the previous log file:
        if remove:
            removeIfExists(self.outputPath)
        # création de l'objet logger qui va nous servir à écrire dans les logs
        logger = logging.getLogger(self.randomName)
        # on met le niveau du logger à DEBUG, comme ça il écrit tout
        logger.setLevel(logging.DEBUG)
        # création d'un formateur qui va ajouter le temps, le niveau
        # de chaque message quand on écrira un message dans le log
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        # création d'un handler qui va rediriger une écriture du log vers
        # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
        file_handler = RotatingFileHandler(self.outputPath, 'a', self.moWeightMax * 1000000, 1)
        # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
        # créé précédement et on ajoute ce handler au logger
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # création d'un second handler qui va rediriger chaque écriture de log
        # sur la console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)
        # We store the logger:
        self.logger = logger

    def prefixText(self, text):
        return self.prefix + str(text)

    def info(self, text):
        self.logger.info(self.prefixText(text))
    def p(self, text):
        self.info(text)
    def log(self, text):
        self.info(text)
    def i(self, text):
        self.info(text)
    def warning(self, text):
        self.logger.warning(self.prefixText(text))
    def w(self, text):
        self.warning(text)
    def e(self, text):
        self.error(text)
    def error(self, text):
        self.logger.error(self.prefixText(text))

    def getLogger(self):
        return self.logger

