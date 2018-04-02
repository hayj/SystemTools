# coding: utf-8
# http://sametmax.com/ecrire-des-logs-en-python/

# pew in st-venv python ~/Workspace/Python/Utils/SystemTools/systemtools/logger.py

import logging
from logging.handlers import RotatingFileHandler
from systemtools.location import *
from systemtools.system import *
from systemtools.basics import *
from systemtools.file import *
from enum import Enum
import traceback
import smtplib
import unidecode


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
        logger, obj = obj, logger
    if logger is not None and not isinstance(logger, Logger):
        logger, obj = obj, logger
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
    def __init__(self, outputPath=None, moWeightMax=1, prefix=None, remove=False, doPrint=True):
        self.prefix = prefix
        if self.prefix is None:
            self.prefix = ""
        self.outputPath = outputPath
        if self.outputPath is None:
            self.outputPath = tmpDir() + "/noname.log"
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
        if doPrint:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            logger.addHandler(stream_handler)
        # We store the logger:
        self.logger = logger

    def remove(self, minSlashCount=3):
        if isFile(self.outputPath):
            remove(self.outputPath, minSlashCount=minSlashCount)
        if isFile(self.outputPath + ".1"):
            remove(self.outputPath, minSlashCount=minSlashCount)

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

    def __repr__(self):
        return str("Logger " + str(self.outputPath))

    def getLogger(self):
        return self.logger



def notif(subject, content="", to=None, logger=None, verbose=True, name='HJWeb Watcher', sender='hjwebwatcher@gmail.com', password=None, doPrint=False, test=False, doStripAccents=True):
    if not isinstance(subject, str):
        subject = lts(subject)
    if not isinstance(content, str):
        content = lts(content)
    if subject is not None:
        subject = subject.strip()
    if subject is not None and content is None:
        if "\n" in subject:
            content = subject
            subject = None
    try:
        if to is None:
            to = sender
            toName = name
        else:
            toName = "You"
        if password is None:
            try:
                from datatools.dataencryptor import DataEncryptor
                password = DataEncryptor()["gmailauth"][sender]
            except Exception as e:
                logException(e, logger, verbose=verbose)
        newline = "\n"
        email = \
"""From: %s <%s>
To: %s <%s>
Subject: %s

%s
""" % (name, sender, toName, to, subject, content)
        if doStripAccents:
            email = unidecode.unidecode(email)
        if doPrint and not test:
            log(subject + "\n" + content, logger, verbose=verbose)
        if test:
            log("<TEST MODE>\n" + subject + "\n" + content, logger, verbose=verbose)
        else:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            # server.starttls() # not working
            server.login(sender, password)
            server.sendmail(sender, to, email)
            server.close()
            # server.quit() # not working
    except Exception as e:
        logException(e, logger, verbose=verbose)
        logError("You probaly have to log to your gmail account and allow recent access. Or connect to https://accounts.google.com/b/0/DisplayUnlockCaptcha and click continue (WARNING: choose the right user after the link redirection by setting the user number of your browser (\"/b/0\" correspond to the first logged user in your browser))")

def test1():
    logger = Logger(tmpDir("teeeest") + "/aaa.txt", doPrint=False)
    for i in range(1000000):
        log(getRandomStr(), logger)

if __name__ == '__main__':
    test1()






