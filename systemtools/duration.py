# coding: utf-8

import time;
import re
from systemtools.basics import *
from threading import Thread


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
    def __init__(self, logger=None, marker="-->", msgSeparator=" | message: ", maxDecimal=2):
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
        if self.logger is not None:
            self.logger.p(text)
        else:
            print(text)

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





