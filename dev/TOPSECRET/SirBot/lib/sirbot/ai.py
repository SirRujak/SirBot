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

class chatHandler:
        ## Needs variables for chatData, command dictionary
        ## Needs functions for loading & unloading command dictionary
        ## Needs fucntions for checking the kind of command it is
        ## Needs functions for splitting up multi commands
        ## Needs functions for adding and removing things from queues
        ## Needs variables for in and out queues
        ## Needs to implement parser and chat level checker
        ## Needs to be able to run at arbitrary chat level
        ## Needs to be able to make a timer
        ## Needs to have all of the base functions made
        ## Base functions are timeout, ban, promote to level, demote to level,
        ## Needs channelName, temp, modList, spamLevel, spamFilter variables where temp is the message
        def __init__():
                pass
        
        def checkChatCMD(chatData):
                pass

        def splitMultiCMD(multiCMD):
                pass

class spamFilter():
        def __init__(self, currentLevel, filterHolder = {'zero':[]}):
                self.currentLevel = currentLevel
                self.filterHolder = filterHolder
        def addNewLevel(self, newLevel, levelData): ## Make sure to pass a string "LEVEL-*" and a list [level,data]
                self.filterHolder[newLevel] = levelData
        def loadLevels(self, spamFileName):
                try:
                        spamFile = open(spamFileName, 'r')
                except FileNotFoundError:
                        print("Your spam filter information has not been found. Check in the config file to make sure the names match.")
##
                        UI.terminalOutput("Your spam filter information has not been found.")
                        return()
                spamDict = json.load(spamFile)
                spamFile.close()
                self.filterHolder.update(spamDict)
        def delLevels(self, levelToDelete):
                del self.filterHolder[levelToDelete]
        def saveLevels(self, spamFileName):
                spamFile = open(spamFileName, 'w')
                json.dumps(self.filterHolder, spamFile)
                spamFile.close()

