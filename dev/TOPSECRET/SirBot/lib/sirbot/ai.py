# -*- coding: utf-8 -*-

#classes containing machinery for artifically intelligent operations
#i.e. data parsing and command execution
from time import time

class baseTimer():
        def __init__(self, currTime, timerLen,
                     chatHandler, commandData,
                     channel, holderLoopBack,
                     timerName):
                self.timerName = timerName
                self.holderLoopBack = holderLoopBack
                self.channel = channel
                self.commandData = commandData
                self.chatHandler = chatHandler
                self.prevTime = nextTime
                self.currTime = currTime
                self.timerLen = timerLen
                self.nextTime = currTime + timerLen
        def setCurrTime(self, currTime):
                self.currTime = currTime
        def setTimerLen(self, timerLen):
                self.timerLen = timerLen
        def checkIfTimePassed(self):
                timeLeft = self.nextTime - self.currTime
                if ( timeLeft <= 0):
                        self.doAction()
        def doAction(self):
                tempList = [0,self.channel,self.currTime,self.commandData,True,
                            None]
                self.chatHandler.enQueue(tempList)
                self.holderLoopBack.reQueue(self.timerName)

class timerHolder():
        def __init__(self, chatHandler, channel):
                self.activeTimerList = []
                self.activeTimerListDeactKey = {}
                self.timersForDeletion = {}
                self.inactiveTimerDict = {}
                self.resetQueue = Queue()
                self.timerNames = {}
                self.chatHandler = chatHandler
                self.channel = channel
                pass

        def startup():
                pass

        def tick():
                ## need to check for:
                ## items being deactivated
                ## items being deleted
                pass

        def idletick():
                pass

        def shutdown():
                pass

        def getCurrentTime():
                return(time())

        def activateTimer(self, timerName):
                tempItem = self.inactiveTimerDict[timerName]
                del self.inactiveTimerDict[timerName]
                self.timerEnQueue(tempItem)

        def timerEnQueue(self, queueItem):
                tempTimeRemainingOnItem = queueItem.nextTime
                tempFoundSpot = 0
                tempCounter = 0
                tempActiveList = self.activeTimerList
                while (tempFoundSpot != 1):
                        if (len(tempActiveList) == 0):
                                tempFoundSpot = 1
                        else:
                                if (tempTimeRemainingOnItem <= tempActiveList[tempCounter].nextTime):
                                        tempFoundSpot = 1
                                else:
                                        tempCounter += 1
                self.activeTimerList.insert(tempCounter, queueItem)

        def deactivateTimer(self, timerName):
                self.activeTimerListDeactKey.add(timerName)

        def createAndActivateTimer(self, timerInfoList):
                tempResult = self.createTimer(timerInfoList)
                if (tempResult == 0):
                        self.activateTimer(timerInfoList[0])
                        return 0
                else:
                        return 1

        def createTimer(self, timerInfoList):
                ## timerInfoList will contain [name, amount of time, commands]
                ## time is in form [HH, MM, SS]
                if (timerInfoList[0] in self.timerNames):
                        return 1
                else:
                        ## self, currTime, timerLen,
                        ## chatHandler, commandData,
                        ## channel, holderLoopBack,
                        ## timerName
                        tempLen = self.timeToSeconds(timerInfoList[1])
                        tempTimer = baseTimer(self.getCurrentTime(),
                                              tempLen, self.chatHandler,
                                              timerInfoList[2], self.channel,
                                              self, timerInfoList[0])
                        self.inactiveTimerDict[timerInfoList[0]] = tempTimer
                        self.timerNames.add(timerInfoList[0])
                        return 0

        def timeToSeconds(combinedTime):
                tempSeconds = combinedTime[0] * 3600 + combinedTime[1] * 60 + combinedTime[2]
                return tempSeconds

        def deleteTimer(self, timerName):
                if (timerName in self.timerNames):
                        if (timerName in self.inactiveTimerDict):
                                del self.inactiveTimerDict[timerName]
                        else:
                                self.timerForDeletion.add(timerName)
                                self.activeTimerListDeactKey.add(timerName)
                        

        def createTimerDict(self):
                pass

        def deleteTimerDict(self):
                pass

        def loadTimerDict(self):
                pass

        def unloadTimerDict(self):
                pass

        def saveTimerDict(self):
                pass

        def reQueue(self, timerName):
                tempTimer = self.activeTimerList.pop()
                self.timerEnQueue(tempTimer)

        
###############################################################
###############################################################



##Types of output:
##normal chat message = "MESSAGE"
##command message = "COMMAND"
##internal message = "INTERNAL"
## NEW COMMAND PARSING AREA
class chatHandler:
        ## DONE Needs variables for chatData, command dictionary
        ## DONE Needs functions for loading & unloading command dictionary
        ## Needs fucntions for checking the kind of command it is
        ## LATER Needs functions for splitting up multi commands
        ## Needs functions for adding and removing things from queues
        ## DONE Needs variables for in and out queues
        ## Needs to implement parser and chat level checker
        ## Needs to be able to run at arbitrary chat level
        ## LATER Needs to be able to make a timer
        ## Needs to have all of the base functions made
        ## Base functions are timeout, ban, promote to level, demote to level,
        ## Needs channelName, temp, modList, spamLevel, spamFilter variables where temp is the message
        def __init__(self, channelName):
                self.boundChannel = channelName
                
                self.commandDictionaryFileName = ''
                self.commandDictionaryFile = None
                self.userLevelDictionary = None
                self.inputQueue = Queue()
                self.outputQueue = Queue()
                self.commandDictionary = {}
                self.spamDictionary = {}
                self.twitchDictionaryFileName = ''
                self.twitchDictionaryFile = None
                self.twitchCommandDictionary = {}
                self.timerList = []
                self.timerListFile = None
                self.timerListFileName = ''
                pass

        ## Base functions that must be in the API. ##
        ## Skip this one for now
        ## Timer input list = [name, currTime, timerLen, chatHandler, commandData, channel]
        
        def createTimer(self, timerData):
                pass

        def deleteTimer(self, timerKey):
                pass

        def checkTimers(self):
                pass
        
        def banUser(self, userData):
                tempString = self.twitchCommandDictionary['BAN']
                tempString = tempString.substitute(userName = userData)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def unbanUser(self, userData):
                tempString = self.twitchCommandDictionary['UNBAN']
                tempString = tempString.substitute(userName = userData)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def activateSlow(self, timeData):
                tempString = self.twitchCommandDictionary['SLOW']
                tempString = tempString.substitute(duration = timeData)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def deactivateSlow(self):
                tempString = self.twitchCommandDictionary['SLOWOFF']
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def activateSubMode(self):
                tempString = self.twitchCommandDictionary['SUBSCRIBERS']
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def deactivateSubMode(self):
                tempString = self.twitchCommandDictionary['SUBSCRIBERSOFF']
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def clearChat(self):
                tempString = self.twitchCommandDictionary['CLEAR']
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def startCommercial(self, timeData):
                if (timeData != None):
                        tempDict = dict(duration = timeData)
                else:
                        tempDict = dict(duration = '30')
                tempString = self.twitchCommandDictionary['COMMERCIAL']
                tempString = tempString.substitute(tempDict)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def hostChannel(self, channelData):
                tempString = self.twitchCommandDictionary['SLOW']
                tempString = tempString.substitute(channelName = channelData)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def unhostChannel(self):
                tempString = self.twitchCommandDictionary['UNHOST']
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def demoteUserToLevel(self, userData, level, mod):
                if (mod == False):
                        self.makeUserViewer(userData)
                tempOut = outputContainer("INTERNAL", level, "SETLEVEL")
                ## Change "SETLEVEL" to the SETLEVEL code once made
                self.addToOutputQueue(tempOut)

        def promoteUserToLevel(self, userData, level, mod):
                if (mod == True):
                        self.makeUserMod(userData)
                tempOut = outputContainer("INTERNAL", level, "SETLEVEL")
                ## Change "SETLEVEL" to the SETLEVEL code once made
                self.addToOutputQueue(tempOut)

        def makeUserMod(self, userData):
                tempString = self.twitchCommandDictionary['MOD']
                tempString = tempString.substitute(userName = userData)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def makeUserViewer(self, userData):
                tempString = self.twitchCommandDictionary['UNMOD']
                tempString = tempString.substitute(userName = userData)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.outputQueue.put(tempOut)

        def timeoutUser(self, userData, timeData):
                if (timeData != None):
                        tempDict = dict(userName = userData,
                                        duration = timeData)
                else:
                        tempDict = dict(userName = userData,
                                        duration = '600')
                tempString = self.twitchCommandDictionary['TIMEOUT']
                tempString = tempString.substitute(tempDict)
                tempOut = outputContainer("COMMAND", tempString, None)
                self.addToOutputQueue(tempOut)

        def activateNotification(self, notificationType):
                ## Time for pseudocode!!! :D
                ## tempOut = outputContainer('INTERNAL', [notificationType, 1], NOTIFICATIONCODE)
                ## self.addToOutputQueue(tempOut)
                pass

        def deactivateNotification(self, notificationType):
                ## Time for pseudocode!!! :D
                ## tempOut = outputContainer('INTERNAL', [notificationType, 0], NOTIFICATIONCODE)
                ## self.addToOutputQueue(tempOut)
                pass

        def createCommand(self, commandKey, resposneValue,
                          commandLevel, callLevel):
                pass

        def deleteCommand(self, commandKey, commandLevel, callLevel):
                pass

        ## Command Level is optional, None give all levels.
        def listCommands(self, commandLevel):
                pass

        ## Funcitons that should possibly be in the API. ##
        def joinChannel(self, channelData):
                pass

        def leaveChannel(self, channelData):
                pass

        ## Other functions. ##
        def checkChatCMD(self, chatData):
                pass

        def updateCommandDict(self):
                pass

        def openCommandDictFile(self):
                pass
        
        def loadCommandDict(self):
                tempString = self.commandDictionaryFile.read()
                self.commandDictionary = json.loads(tempString)

        def delCommandDict(self):
                self.commandDictionary = {}

        ## NEED TO FIX THIS ONE
        def loadTwitchDict(self, dictFile):
                tempString = dictFile.read()
                self.twitchCommandDictionary = json.loads(tempString)
                pass

        def delTwitchDict(self):
                self.twitchCommandDictionary = {}

        def addToOutputQueue(self, leavingData):
                self.outputQueue.put(leavingData)

        def enQueue(self, data):
                self.addToInputQueue(data)

        def addToInputQueue(self, data):
                tempData = chatDataMessage(data)
                self.inputQueue.put(tempData)

        def removeFromInputQueue(self):
                tempHolder = self.inputQueue.get()
                self.checkChatCMD(tempHolder)

        ## Split a multiple command line into multiple single commands.
        def splitMultiCMD(self, multiCMD):
                newCMDs = multiCMD.messageContents.split('\&')
                for CMD in newCMDs:
                        multiCMD.messageContents = CMD
                        self.addToInputQueue(multiCMD)

        def setBoundChannel(self, channelName):
                this.boundChannel = channelName

## Secondary classes.
class chatDataMessage:
##        def __init__(self, userName, channelInfo, timeStamp, messageContents,
##                     isLocal, chatType):
        def __init__(self, infoList):
                self.userName = infoList[0]
                self.channelInfo = infoList[1]
                self.timeStamp = infoList[2]
                self.messageContents = infoList[3]
                self.isLocal = infoList[4]
                self.chatType = infoList[5]

class outputContainer:
        def __init__(self, chatType, message, subType):
                self.chatType = chatType
                self.message = message
                self.subType = subType
                

class channelData:
        def __init__():
                pass


###############################################################
###############################################################


                
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

