# coding: utf-8

# pew in st-venv python /home/hayj/Workspace/Python/Utils/SystemTools/systemtools/duration.py

import time
import re
from systemtools.logger import *
from systemtools.basics import *
from threading import Thread
import os
import sys
from enum import Enum
import signal


class Timer:
    def __init__(self, callback, interval, *args, sleepFirst=False, sleepCount=1000, **kwargs):
        """
            interval in seconds
        """
        self.sleepCount = sleepCount
        self.interval = interval
        self.callback = callback
        self.stopped = True
        self.firstExec = True
        self.sleepFirst = sleepFirst
        self.mainThread = None
        self.setArgs(*args, **kwargs)

    def setArgs(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def isRunning(self):
        return not self.stopped

    def sleep(self):
        sleepPart = self.interval / self.sleepCount
        for i in range(self.sleepCount):
            if self.isRunning():
                time.sleep(sleepPart)

    def run(self):
        self.stopped = False
        while not self.stopped:
            if self.firstExec and self.sleepFirst:
                self.sleep()
            if self.isRunning():
                self.callback(*self.args, **self.kwargs)
            self.sleep()
            self.firstExec = False

    def start(self):
        self.firstExec = True
        self.mainThread = Thread(target=self.run)
        self.mainThread.start()

    def stop(self):
        self.stopped = True



class TicToc():
    """
        This class provide 2 methods to print time during an execution
    """
    def __init__(self, verbose=True, logger=None, marker="-->", msgSeparator=" | message: ", maxDecimal=2):
        self.verbose = verbose
        self.logger = logger
        self.startTime = None;
        self.previousTime = None;
        self.marker = marker;
        self.msgSeparator = msgSeparator;
        self.maxDecimal = maxDecimal;

    def setMaxDecimal(self, maxDecimal):
        self.maxDecimal = maxDecimal;

    def tic(self, msg=None, display=True):
        """
            This method start the timer and print it, or print the time between the previous tic()
            and the current tic(). You can print a message by giving it in parameters.
            It's the local duration.
        """
        if msg is None:
            msg = "";
        else:
            msg = self.msgSeparator + msg;
        if self.startTime is None:
            self.startTime = time.time();
            self.previousTime = self.startTime;
            if display:
                self.p(self.marker + " tictoc starts..." + msg);
            return -1;
        else:
            currentTime = time.time();
            diffTime = currentTime - self.previousTime;
            diffTime = float(float(int(diffTime * (10**self.maxDecimal))) / float((10**self.maxDecimal)));
            if display:
                self.p(self.marker + " tic: " + secondsToHumanReadableDuration(diffTime) + msg); # time duration from the previous tic()
            self.previousTime = currentTime;
            return diffTime;

    def toc(self, msg=None, display=True):
        """
            This method print the elapsed time from the first tic().
            You can print a message by giving it in parameters.
            It's the total duration.
        """
        if self.startTime is not None:
            if msg is None:
                msg = "";
            else:
                msg = self.msgSeparator + msg;
            currentTime = time.time();
            diffTime = currentTime - self.startTime;
            diffTime = float(float(int(diffTime * (10**self.maxDecimal))) / float((10**self.maxDecimal)));
            if display:
                self.p(self.marker + " toc total duration: " + secondsToHumanReadableDuration(diffTime) + msg);
            return diffTime;
        return -1;

    def p(self, text):
        log(text, self)
        # if self.logger is not None:
        #     self.logger.p(text)
        # else:
        #     print(text)

def secondsToHumanReadableDuration(seconds):
    """
        :example:
        >>> secondsToHumanReadableDuration(0.1)
        '0.1s'
        >>> secondsToHumanReadableDuration(10)
        '10.0s'
        >>> secondsToHumanReadableDuration(10.2)
        '10.2s'
        >>> secondsToHumanReadableDuration(3600)
        '1h 0m 0.0s'
        >>> secondsToHumanReadableDuration(7210)
        '2h 0m 10.0s'
        >>> secondsToHumanReadableDuration(7270)
        '2h 1m 10.0s'
    """
    m, s = divmod(seconds, 60.0)
    h, m = divmod(m, 60.0)
    h = int(h)
    m = int(m)
    result = ""
    if h != 0:
        result += str(h) + "h "
        result += str(m) + "m "
    elif m != 0:
        result += str(m) + "m "
    result += floatAsReadable(truncateFloat(s, 3)) + "s"
    return result





OUTPUT_TYPE = Enum("OUTPUT_TYPE", "standard subl nohup logger")
def getOutputType(logger=None):
    if logger is not None:
        return OUTPUT_TYPE.logger
    if signal.getsignal(signal.SIGHUP) == signal.SIG_DFL:
        try:
            size = os.get_terminal_size()
        except:
            return OUTPUT_TYPE.subl
        return OUTPUT_TYPE.standard
    else:
        return OUTPUT_TYPE.nohup

def canCleanOutput(*args, **kwargs):
    return getOutputType(*args, **kwargs) == OUTPUT_TYPE.standard

class ProgressBar:
    def __init__\
    (
        self,
        iterationAmount,
        message=None,
        printRatio=None, # Auto
        logger=None,
        verbose=True,
        defaultPrintRatio=0.1,
        progressSymbol="=",
        progressSymbolAmount=20,
        printProgressBar=True,
        printFloatingPoint=None, # Auto
    ):
        self.printFloatingPoint = printFloatingPoint
        self.progressSymbolAmount = progressSymbolAmount
        self.printProgressBar = printProgressBar
        self.progressSymbol = progressSymbol
        self.iterationAmount = iterationAmount
        self.message = message
        self.printRatio = printRatio
        self.logger = logger
        self.verbose = verbose
        self.outputType = getOutputType(logger=self.logger)
        self.canCleanOutput = canCleanOutput(logger=self.logger)
        if self.printRatio is None:
            if self.outputType == OUTPUT_TYPE.standard:
                self.printRatio = 0.0001
            else:
                self.printRatio = defaultPrintRatio
        if self.printFloatingPoint is None:
            if self.canCleanOutput or self.printRatio < 0.01:
                self.printFloatingPoint = True
            else:
                self.printFloatingPoint = False
        self.tt = TicToc(verbose=False)
        self.tt.tic()
        self.currentIteration = 0
        self.durationHistory = []
        if self.iterationAmount == 0:
            self.toc()
        if self.iterationAmount < 200:
            self.printFloatingPoint = False

    def tic(self, extraMessage=None, minRatioForRemainingMessage=0.1):
        duration = self.tt.tic()
        self.durationHistory.append(duration)
        totalDuration = self.tt.toc()
        self.currentIteration += 1
        if self.iterationAmount == 0:
            logWarning("The iterationAmount is 0.", self)
            return duration
        if self.currentIteration == self.iterationAmount:
            self.toc()
            return duration
        doneRatio = self.currentIteration / self.iterationAmount
        theModulo = int(self.printRatio * self.iterationAmount)
        if theModulo == 0:
            theModulo = 1
        hasToDisplay = self.currentIteration == 1 or self.currentIteration % theModulo == 0
        if hasToDisplay:
            text = ""
            if self.message is not None:
                text += self.message + " "
            if not self.printFloatingPoint:
                percent = math.floor(doneRatio * 100)
                aSpace = ""
                if percent < 10:
                    aSpace = " "
                percent = " " + aSpace + str(percent)
            else:
                percent = str(int(doneRatio * 100 * 100 + 100000))
                percent = percent[2:]
                if percent.startswith("0"):
                    percent = " " + percent[1:]
                percent = percent[:2] + "." + percent[2:]

                # percent = str(int((truncateFloat(doneRatio * 100, self.floatingPointAmount) + 100000) * 100))
                # percent = percent[1:]
                # if len(percent) == 5:
                #     percent = percent[:2] + "." + percent[2:]
                # else:
                #     percent = " " + percent[:1] + "." + percent[1:]
            text += str(percent) + "%"
            if self.printProgressBar:
                nbSymbols = int(doneRatio * self.progressSymbolAmount)
                symbols = self.progressSymbol * nbSymbols + " " * (self.progressSymbolAmount - nbSymbols)
                text += " [" + symbols + "]"
            if extraMessage is not None:
                text += " " + str(extraMessage)
            if doneRatio > minRatioForRemainingMessage:
                remainingSecs = (totalDuration / doneRatio) - totalDuration
                text += " (" + secondsToHumanReadableDuration(remainingSecs) + " left)"
            if self.canCleanOutput:
                print(text, end="\r")
            else:
                log(text, self)
        return duration

    def toc(self, extraMessage=None):
        self.currentIteration = self.iterationAmount
        meanDurationText = secondsToHumanReadableDuration(sum(self.durationHistory)/len(self.durationHistory))
        totalDuration = self.tt.toc()
        totalDurationText = secondsToHumanReadableDuration(totalDuration)
        text = ""
        if self.message is not None:
            text += self.message + " "
        if self.printFloatingPoint:
            text += "  100%"
        else:
            text += "100%"
        if self.printProgressBar:
            symbols = self.progressSymbol * self.progressSymbolAmount
            text += " [" + symbols + "]"
        if extraMessage is not None:
            text += " " + extraMessage
        text += " (total duration: " + totalDurationText + ", mean duration: " + meanDurationText + ")"
        if self.canCleanOutput:
            print(text, end="\r")
            print()
        else:
            log(text, self)
        return totalDuration


def pb(items, iterationAmount=None, **kwargs):
    if iterationAmount is None:
        try:
            iterationAmount = len(items)
        except: pass
    if iterationAmount is None:
        raise Exception("Length of items not found.")
    p = ProgressBar(iterationAmount, **kwargs)
    for current in items:
        yield current
        p.tic()



def test1():
    iterationAmount = 30000
    pb = ProgressBar(iterationAmount, "test", printRatio=0.0001)
    for i in range(iterationAmount):
        pb.tic(i)
        time.sleep(0.00001)


def test2():
    iterationAmount = 20
    pb = ProgressBar(iterationAmount, "test", printRatio=0.0001)
    for i in range(iterationAmount):
        pb.tic(i)
        time.sleep(0.1)


def test3():
    iterationAmount = 20
    pb = ProgressBar(iterationAmount, "test", printRatio=0.5)
    for i in range(iterationAmount):
        pb.tic(i)
        time.sleep(0.1)

def test4():
    iterationAmount = 200
    pb = ProgressBar(iterationAmount)
    for i in range(iterationAmount):
        time.sleep(0.01)
        pb.tic()

# from tqdm import tqdm

# def test5():
#     iterationAmount = 20000
#     # pb = ProgressBar(iterationAmount)
#     for i in tqdm(range(iterationAmount)):
#         time.sleep(0.01)
#         # pb.tic()

# def test6():
#     iterationAmount = 20000000
#     # pb = ProgressBar(iterationAmount)
#     for i in tqdm(range(iterationAmount)):
#         time.sleep(0.0001)
#         # pb.tic()

def test8():
    for i in pb(range(200)):
        time.sleep(0.01)



if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    test8()