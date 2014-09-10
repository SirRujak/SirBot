# -*- coding: utf-8 -*-

#classes containing machinery for artifically intelligent operations
#i.e. data parsing and command execution

class baseTimer():
        def __init__(self, prevTime, currTime, timerLen):
                self.prevTime = prevTime
                self.currTime = currTime
                self.timerLen = timerLen
                self.timePassed = 0
        def setCurrTime(self, currTime):
                self.currTime = currTime
        def setTimerLen(self, timerLen):
                self.timerLen = timerLen
        def checkIfTimePassed(self):
                timePass = self.currTime - self.prevTime
                if ( timePass >= self.timerLen):
                        self.timePassed = 1
                else:
                        self.timePassed = 0

