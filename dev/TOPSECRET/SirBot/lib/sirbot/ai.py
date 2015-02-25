# -*- coding: utf-8 -*-

#classes containing machinery for artifically intelligent operations
#i.e. data parsing and command execution
from random import choice
import json
from time import time
import queue
from os import makedirs

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
        def setNextTime(self):
                self.nextTime = self.currTime + self.timerLen
        def checkIfTimePassed(self):
                timeLeft = self.nextTime - self.currTime
                if ( timeLeft <= 0):
                        self.setNextTime()
                        self.doAction()
                        return 1
                else:
                        return 0
        def doAction(self):
                tempList = [0,self.channel,self.currTime,self.commandData,True,
                            None]
                tempContainer = chatDataMessage(tempList)
                self.chatHandler.enQueue(tempContainer)
                self.holderLoopBack.reQueue(self.timerName)

class timerHolder():
        def __init__(self, chatHandler, channel, timerDictFile):
                self.activeTimerList = []
                self.activeTimerListDeactKey = {}
                self.timersForDeletion = {}
                self.inactiveTimerDict = {}
                self.inQueue = queue.Queue()
                self.timerNames = ()
                self.chatHandler = chatHandler
                self.channel = channel
                ## Make sure this is opened in read and write mode
                self.timerDictFile = open(timerDictFile, 'r+')
                self.alteredTimers = 0
                self.currentTimerValues = {}

        def tick(self):
                ## need to check for:
                ## items being deactivated
                ## items being deleted
                ## is it time to work on the new one?
                if self.timersForDeletion:
                        for item in self.timersForDeletion:
                                self.deleteTimer(item)
                if (self.activeTimerList):
                        if (len(self.activeTimerList[0]) != 0):
                                if self.activeTimerList[0] in self.activeTimerListDeactKey:
                                        tempTimer = self.activeTimerList.pop()
                                        self.inactiveTimerDict[tempTimer.timerName] = tempTimer
                                else:
                                        tempResponse = self.checkIfTimerChanged()
                                        if (tempResponse == 0):
                                                if (self.activeTimerList[0].checkIfTimePassed() == 1):
                                                        self.reQueue()
                                        else:
                                                self.activeTimerList.pop()

        def checkIfTimerChanged(self):
                tempTimer = self.activeTimerList[0]
                tempValues = self.currentTimerValues[tempTimer.timerName]
                if (tempTimer.timeLen == tempValues[0] and tempTimer.commandData == tempValues[1]):
                        return 0
                else:
                        return 1

        def idletick(self):
                if self.inQueue.empty():
                        pass
                else:
                        tempMessage = self.inQueue.get()
                        ## Add new timer
                        if (tempMessage[0] == 0):
                                ## tempMessage = [type, name, [HH, MM, SS], command, startsActive]
                                ## startsActive: 1-true, 0-false
                                if (tempMessage[4] == 1):
                                        self.createAndActivateTimer(tempMessage[1:4])
                                else:
                                        self.createTimer(tempMessage[1:4])
                        ## Delete timer
                        elif (tempMessage[0] == 1):
                                ## tempMessage = [type, name]
                                self.deleteTimer(tempMessage[1])
                        ## Alter timer
                        elif (tempMessage[0] == 2):
                                ## tempMessage = [type, name, [HH, MM, SS], command]
                                self.alterTimer(tempMessage[2:])

        def shutdown(self):
                self.saveTimerDict()

        def startup(self):
                self.loadTimerDict()

        def alterTimer(self,infoList):
                del self.timerNames[activeTimerList[0]]
                self.createAndActivateTimer(infoList)

        def getCurrentTime():
                return(time())

        def activateTimer(self, timerName):
                if timerName in self.activeTimerListDeactKey:
                        del self.activeTimerListDeactKey[timerName]
                else:
                        if timerName in self.inactiveTimerDict:
                                pass
                        else:
                                tempItem = self.inactiveTimerDict[timerName]
                                del self.inactiveTimerDict[timerName]
                                self.timerEnQueue(tempItem)

        def checkTimers(self):
                tempDict = {}
                tempList = []
                for item in self.activeTimerList:
                        tempList.append(item)
                tempDict['ACTIVE'] = tempList
                tempList = []
                for item in self.inactiveTimerDict:
                        tempList.append(item)
                tempDict['INACTIVE'] = tempList
                return tempDict

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
                ## time is in form [HH, MM, SS] or SS
                if (timerInfoList[0] in self.timerNames):
                        return 1
                else:
                        ## self, currTime, timerLen,
                        ## chatHandler, commandData,
                        ## channel, holderLoopBack,
                        ## timerName
                        try:
                                tempLen = self.timeToSeconds(timerInfoList[1])
                        except:
                                tempLen = timerInfoList[0]
                        tempTimer = baseTimer(self.getCurrentTime(),
                                              tempLen, self.chatHandler,
                                              timerInfoList[2], self.channel,
                                              self, timerInfoList[0])
                        self.inactiveTimerDict[timerInfoList[0]] = tempTimer
                        self.timerNames.add(timerInfoList[0])
                        self.currentTimerValues[timerInfoList[0]] = [tempLen,timerInfoList[2]]
                        self.saveTimerDict()
                        return 0

        def timeToSeconds(combinedTime):
                tempSeconds = combinedTime[0] * 3600 + combinedTime[1] * 60 + combinedTime[2]
                return tempSeconds

        def deleteTimer(self, timerName):
                if (timerName in self.timerNames):
                        if (timerName in self.inactiveTimerDict):
                                del self.inactiveTimerDict[timerName]
                                del self.timerNames[timerName]
                                del self.currentTimerValues[timerName]
                                self.saveTimerDict()
                        else:
                                self.timerForDeletion.add(timerName)
                                self.activeTimerListDeactKey.add(timerName)

        ## Not currently in use
        def deleteTimerDict(self):
                self.activeTimerList = []
                self.activeTimerListDeactKey = {}
                self.timersForDeletion = {}
                self.inactiveTimerDict = {}
                self.resetQueue = Queue()
                self.timerNames = {}

        def loadTimerDict(self):
                tempJSON = self.timerDictFile.read()
                tempDict = json.loads(tempJSON)
                tempList = tempDict['ACTIVE-LIST']
                del tempDict['ACTIVE-LIST']
                for item in tempDict:
                        self.createTimer(item)
                for item in tempList:
                        self.activateTimer(item)

        def saveTimerDict(self):
                tempDict = self.inactiveTimerDict
                tempList = []
                for item in self.activeTimerList:
                        tempDict[item.timerName] = item
                        tempList.append(item.timerName)
                #currTime, timerLen,
                     #chatHandler, commandData,
                     #channel, holderLoopBack,
                     #timerName
                tempDict2 = {}
                for item in tempDict:
                        if item in self.alteredTimerDict:
                                tempTime = self.timeToSeconds(self.alteredTimerDict[item][0])
                                tempDict2[item] = [item, tempTime, self.alteredTimeDict[item][1]]
                        else:
                                tempDict2[item] = [tempDict[item].timerName,tempDict[item].timerLen,tempDict[item].commandData]
                tempDict2['ACTIVE-LIST'] = tempList
                tempJSON = json.dumps(tempDict2)
                self.timerDictFile.seek(0)
                self.timerDictFile.write(tempJSON)
                self.timerDictFile.truncate()
                self.timerDictFile.close()

        def reQueue(self):
                tempTimer = self.activeTimerList.pop()
                self.timerEnQueue(tempTimer)


###############################################################
###############################################################



##Types of output:
##normal chat message = "MESSAGE"
##command message = "COMMAND"
##internal message = "INTERNAL"
## NEW COMMAND PARSING AREA
class ai:
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
        def __init__(self):
                self.boundChannel = ''
                self.botName = ''
                self.commandDictionaryFile = None
                self.userLevelDictionary = None
                self.inputQueue = queue.Queue()
                self.outputQueue = queue.Queue()
                self.commandDictionary = {}
                self.timerDictionary = {}
                self.spamDictionary = {}
                self.twitchDictionaryFile = None
                self.twitchCommandDictionary = {}
                self.timerDictFile = None
                self.pathCommandName = ''
                self.pathDefaultCommandName = ''
                self.pathTimerName = ''
                self.pathDefaultTimerName = ''
                self.pathTwitchName = ''
                self.tempKeyList = []
                self.userDict = {}
                self.currentTime = None
                self.currentLine = None
                self.saveCommands = False
                self.lastSave = None
                pass

        def getCurrentTime(self):
            self.currentTime = time()

        ##def startup(self, basePath, channelName, userDict, botName):
        def startup(self,configFile,userDict):
                botName = configFile['Twitch Accounts']['automated account']['name']
                channelName = configFile['Twitch Channels']['default channel']
                basePath = configFile['path']
                self.botName = botName
                self.currentLine = 0
                self.getCurrentTime()
                self.userDict = userDict
                self.makeDictPathName(basePath, channelName) ##channelName, basePath
                self.lastSave = time()
                try:
                        self.openCommandDictFile(self.pathCommandName)
                except:
                    try:
                            self.openCommandDictFile(self.pathDefaultCommandName)
                            makedirs(self.pathCommandFolders)
                            self.updateCommandDict(self.pathCommandName)

                    except Exception as e:
                            return([32,e])
                try:
                        self.openTimerDictFile(self.pathTimerName)
                        self.boundChannel = channelName
                        self.timerHolder = timerHolder(self,channelName,self.pathTimerName)
                        tempCheck = self.timerDictFile.read()
                        #chatHandler, channel, timerDictFile
                        self.timerHolder.startup() ##channelName, timerDictFile
                except Exception as e1:
                    try:
                        self.openTimerDictFile(self.pathDefaultTimerName)
                        self.timerDictValues = self.timerDictFile.read()
                        self.timerDictValues = json.loads(self.timerDictValues)
                        self.timerDictFile.close()
                        makedirs(self.pathTimerFolders)
                        self.updateTimerDict(self.pathTimerName)
                        self.openTimerDictFile(self.pathTimerName)
                        channelName = self.boundChannel
                        self.timerHolder = timerHolder(self,channelName,self.pathTimerName)
                        #chatHandler, channel, timerDictFile
                        self.timerHolder.startup() ##channelName, timerDictFile
                    except Exception as e:
                            return([32,e])
                try:
                        self.openTwitchDictFile()
                except Exception as e:
                        return([32,e])
                return([31,[self.boundChannel,None]])

        def tick(self, data):
                self.timerHolder.tick()
                tempResponse = self.checkChatCMD(data)
                if self.saveCommands:
                    if (time() - self.lastSave > 10):
                        self.updateCommandDict(self.pathCommandName)
                        self.lastSave = time()
                        self.saveCommands = False
                if tempResponse:
                    if tempResponse[1]:
                        tempList = [tempResponse[0],[]]
                        tempList[1].append(self.boundChannel)
                        tempList[1].append(tempResponse[1])
                        return tempList
                    else:
                        return [31,[self.boundChannel,None]]
                else:
                    return [31,[self.boundChannel,None]]

        def idletick(self, data):
                self.timerHolder.idletick()
                if self.saveCommands:
                    if (time() - self.lastSave > 10):
                        self.updateCommandDict(self.pathCommandName)
                        self.lastSave = time()
                        self.saveCommands = False
                return [31,[self.boundChannel,None]]

        def shutdown(self):
                self.timerHolder.shutdown()
                self.updateCommandDict(self.pathCommandName)
                pass

        def checkChat(self, item): ## item is a list of format [type, [list with other stuff]]
                if item:
                        if (item[0] == 1):
                              pass

        def makeDictPathName(self, basePath, channelName):
                self.pathCommandName = basePath + '//data//sirbot//commands//' + channelName + '//commands.json'
                self.pathDefaultCommandName = basePath + '//data//sirbot//commands//defaultCommands//commands.json'
                self.pathCommandFolders = basePath + '//data//sirbot//commands//' + channelName
                self.pathTimerName = basePath + '//data//sirbot//timers//' + channelName + '//timers.json'
                self.pathDefaultTimerName = basePath + '//data//sirbot//timers//defaultTimers//timers.json'
                self.pathTimerFolders = basePath + '//data//sirbot//timers//' + channelName
                self.pathTwitchName = basePath + '//data//sirbot//twitchcommands//twitchcommands.json'

        ## Base functions that must be in the API. ##
        ## Skip this one for now
        ## Timer input list = [name, currTime, timerLen, chatHandler, commandData, channel]

        def createTimer(self, timerData):
                ## timerInfoList will contain [name, amount of time, commands] + [activeNow]
                ## time is in form [HH, MM, SS] or SS
                if (timerData[3] == 0):
                        self.timerHolder.createTimer(timerData[0:3])
                else:
                        self.timerHolder.createAndActivateTimer(timerData[0:3])

        def deleteTimer(self, timerName):
                self.timerHolder.deleteTimer(timerName)

        def changeTimerState(self, timerName, newState):
                if (newState == 0):
                        self.timerHolder.deactivateTimer(timerName)
                else:
                        self.timerHolder.activateTimer(timerName)

        def alterTimer(self, name, time, command):
                ## Name, time, command
                self.timerHolder.inQueue.put([2,name, time, command])

        def checkTimers(self):
                tempDict = self.timerHolder.checkTimers()
                tempList = tempDict['ACTIVE']
                tempString = 'Active timers:'
                for item in tempDict['ACTIVE']:
                        tempString = tempString + ' ' + item
                self.outputText(tempString)
                tempList = tempDict['INACTIVE']
                tempString = 'Inactive timers:'
                for item in tempDict['INACTIVE']:
                        tempString = tempString + ' ' + item
                self.outputText(tempString)

        def outputText(self, outputString):
                tempOut = outputContainer("CHAT", outputString, None)
                self.outputQueue.put(tempOut)

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
                tempString = self.twitchCommandDictionary['HOST']
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

        ## commandList contains commandKey, responseValue, commandLevel, callLevel, isActive, responseKey in that order
        def getOpenInKey(self):
            valFound = False
            tempVal = 1
            while not valFound:
                if (str(tempVal) in self.commandDictionary['LINKDICT']):
                    tempVal += 1
                else:
                    valFound = True
                    return tempVal

        def getOpenOutKey(self):
            valFound = False
            tempVal = 1
            while not valFound:
                if (str(tempVal) in self.commandDictionary['OUTLINKS'] or str(tempVal) in self.tempKeyList):
                    tempVal += 1
                else:
                    valFound = True
                    self.tempKeyList.append(str(tempVal))
                    return tempVal

        def checkIfCommandKeyExists(self, tempKey):
            tempVar = 0
            if (' ' not in tempKey):
                if tempKey in self.commandDictionary['CMDS']:
                    tempVar = 1
                else:
                    tempVar = 0
            else:
                splitKey = tempKey.split(' ')
                tempDict = self.commandDictionary['CMDS']
                for i in range(len(splitKey)-1):
                    if splitKey[i] in tempDict:
                        tempDict = tempDict[splitKey[i]]
                    else:
                        tempVar = 0
                if splitKey[-1] in tempDict:
                    tempVar = 1
                else:
                    tempVar = 0
            if (tempVar == 1):
                return 1
            else:
                return 0

        def checkIfResponseExists(self, tempResponse):
            tempList = []
            for i in range(len(tempResponse)):
                if tempResponse[i] in self.commandDictionary['RESPONSEDICT']:
                    tempList.append(self.commandDictionary['RESPONSEDICT'][tempResponse[i]][0][0])
                else:
                    tempList.append(None)
            return tempList

        def sortResponseLimits(self, tempLimits):
            for i in range(len(tempLimits)):
                if tempLimits[i][0] == None:
                    tempLimits[i][1] = 0
                else:
                    tempLimits[i][1] = int(tempLimits[i][1])
            sortedLimits = sorted(tempLimits, key=lambda x: x[1])
            sortedLimits.reverse()

            for i in range(len(sortedLimits)):
                    if sortedLimits[i][1] == 0:
                        sortedLimits[i][1] = None
                    else:
                        sortedLimits[i][1] = str(sortedLimits[i][1])
            return(sortedLimits)

        def checkForEmptySlots(self, inputItems):
            for i in range(len(inputItems)):
                if (inputItems[i] == None):
                    if (i == 2):
                        inputItems[i] = ['everyone']
                    elif (i == 4):
                        inputItems[i] = '1'
                    elif (i == 5):
                        inputItems[i] = '-1'
                    elif (i == 6):
                        inputItems[i] = '-1'
                    elif (i == 7):
                        inputItems[i] = [['>','-1']]
                    elif (i == 8):
                        inputItems[i] = '0'
                    elif (i == 9):
                        inputItems[i] = 'group.default'
            inputItems[2] = [inputItems[2][0].lower()]
            return inputItems

        def checkAllValues(self, filledEntries):
            if None in filledEntries:
                return 1
            else:
                return None

        def createDictNest(self, tempList, dictLocation):
            if tempList:
                tempItem = tempList.pop(0)
                if tempItem in dictLocation:
                    pass
                else:
                    dictLocation.update({tempItem:{}})
                returnLocation = self.createDictNest(tempList,dictLocation[tempItem])
                return 1
            else:
                return 1


        ## commandLevel should be a set containing all the desired command levels
        def makeNewEntry(self,inputItems):##,commandKey,responseValue,commandLevel,
                         ##callLevel,isActive,lineLimit,timeLimit,responseLimits):
            filledEntries = self.checkForEmptySlots(inputItems)
            if (len(filledEntries) == 10):

                commandKey = inputItems[0]
                responseValue = inputItems[1]
                commandLevel = inputItems[2]
                callLevel = inputItems[3]
                isActive = inputItems[4]
                lineLimit = inputItems[5]
                timeLimit = inputItems[6]
                responseLimits = inputItems[7]
                accessLevel = inputItems[8]
                subGroup = inputItems[9].split(' ')

                toContinue = self.checkAllValues(filledEntries)
                if (commandKey == 'REMAINDER' or commandKey == 'TEMPVAL'):
                    toContinue = 1

                if not self.checkIfCommandKeyExists(commandKey) and not toContinue:
                    ## Check to see if response or command exists if not make them
                    ## and their links.
                    tempOutKey = self.checkIfResponseExists(responseValue)
                    tempInKey = self.getOpenInKey()
                    self.tempKeyList = []
                    tempTypeList = []
                    for i in range(len(tempOutKey)):
                        if (tempOutKey[i] == None):
                            tempOutKey[i] = self.getOpenOutKey()
                    for i in range(len(responseValue)):

                        if '\&' in responseValue[i]:
                            tempTypeList.append(1)
                        else:
                            tempTypeList.append(0)

                    ## Check to see if the command levels exist and if not make them
                    if self.commandDictionary["LVLS"]:
                        for i in range(len(commandLevel)):
                            if not commandLevel[i] in self.commandDictionary["LINKS"]:
                                self.commandDictionary["LVLS"].append(commandLevel[i])
                                self.commandDictionary["LINKS"][commandLevel[i]] = {'INFO':{'ACCESSLEVEL':accessLevel,'CREATOR':callLevel}}
                    else:
                        for i in range(len(commandLevel)):
                            self.commandDictionary["LVLS"].append(commandLevel[i])
                            self.commandDictionary["LINKS"][commandLevel[i]] = {'INFO':{'ACCESSLEVEL':accessLevel}}

                    ## Add command to the 'CMDS' dict
                    tempSpecialSet = set(['ACTIVATINGUSER',
                                         'CHANNEL',
                                         'BOTNAME',
                                         'REMAINDER',
                                         'USERNAME',
                                         'TEMPVAL'])
                    if ' ' in commandKey:
                        tempKey = commandKey.split(' ')
                        tempKey2 = commandKey.split(' ')
                        self.createDictNest(tempKey, self.commandDictionary['CMDS'])
                        finalLocation = self.commandDictionary['CMDS']
                        for i in range(len(tempKey2)-1):
                            if tempKey2[i] not in tempSpecialSet:
                                tempKey2[i] = tempKey2[i].lower()
                            finalLocation = finalLocation[tempKey2[i]]
                        if not finalLocation[tempKey2[-1]]:
                            finalLocation[tempKey2[-1]] = {}
                        finalLocation[tempKey2[-1]].update({"COMMAND":{"LINK":str(tempInKey),"ACTIVE":isActive,"LASTLINE":"0","LASTTIME":"0","TOTAL":"0"}})
                        self.saveCommands = True
                    else:
                        if commandKey not in tempSpecialSet:
                            commandKey = commandKey.lower()
                        tempDict = self.commandDictionary['CMDS']
                        tempDict[commandKey] = {}
                        tempDict[commandKey]['COMMAND']={"LINK":str(tempInKey),
                                                         "ACTIVE":isActive,
                                                         "LASTLINE":"0",
                                                         "LASTTIME":"0",
                                                         "TOTAL":"0"}

                    ## Add links to OUTLINKS
                    for i in range(len(tempOutKey)):
                        if str(tempOutKey[i]) not in self.commandDictionary['OUTLINKS']:
                            self.commandDictionary['OUTLINKS'].append(str(tempOutKey[i]))
                    ## Add links to LINKDICT
                    tempOutStrKey = []
                    for i in range(len(tempOutKey)):
                        tempOutStrKey.append(str(tempOutKey[i]))
                    self.commandDictionary['LINKDICT'][str(tempInKey)] = tempOutStrKey
                    ## Add links to CONDITIONS
                    tempLimits = self.sortResponseLimits(responseLimits)
                    self.commandDictionary['CONDITIONS'][str(tempInKey)] = str(tempLimits)
                    ## Add info for RESPONSEDICT
                    for i in range(len(responseValue)):
                        if str(responseValue[i]) in self.commandDictionary['RESPONSEDICT']:
                            self.commandDictionary['RESPONSEDICT'][str(responseValue[i])][1].append(str(tempInKey))
                        else:
                            self.commandDictionary['RESPONSEDICT'][str(responseValue[i])] = [[str(tempOutKey[i])],[str(tempInKey)]]
                    ## Add info for sub groups
                    ## Add info for LINKS
                    ## Need to fix!!!
                    tempGroupList = {}
                    tempUserList = {}
                    for item in range(len(subGroup)):
                        if 'group.' in subGroup[item]:
                            tempGroupList.update({subGroup[item].split('group.')[1]:'0'})
                        else:
                            tempUserList.update({subGroup[item]:'0'})
                    tempGroupList.update({'owner':'0'})
                    for i in range(len(tempOutKey)):
                        tempString = str(tempOutKey[i])
                        try:
                            self.commandDictionary['LINKS'][commandLevel[0]]
                        except:
                            self.commandDictionary['LINKS'][commandLevel[0]] = {}
                        self.commandDictionary['LINKS'][commandLevel[0]][tempString] = {"RESPONSE":responseValue[i],
                                                                                                     "TYPE":str(tempTypeList[i]),
                                                                                                     "LIMITS":{"LENGTH":str(lineLimit),
                                                                                                               "TIME":str(timeLimit)},
                                                                                                     'CREATOR':callLevel,
                                                                                                     'LASTEDITOR':'',
                                                                                                     'USERS':tempUserList,
                                                                                                     'GROUPS':tempGroupList}
                        self.saveCommands = True
                else:
                    return [31,[self.boundChannel, None]]
                    ## Change this to deal with ones that are there and you are editing them
                    ## pretty much, take what is there and then change anything that was passed
                    ## otherwise leave things the same and change the editor

        def parseForNewCommand(self, commandString, userName):
            tempCommandList = commandString.split(' -')
            tempItems = []
            for i in range(len(tempCommandList)):
                tempItems.append(tempCommandList[i].split(':', 1))
            finalList = [None]*10
            for i in range(len(tempItems)):
                if (tempItems[i][0] == 'cmd'):
                    if (tempItems[i][1] == ''):
                        finalList[0] = None
                    else:
                        finalList[0] = tempItems[i][1]
                elif (tempItems[i][0] == 'response'):
                    if (tempItems[i][1] == ''):
                        finalList[1] = None
                    else:
                        if (len(tempItems[i][1]) == 1):
                            finalList[1] = [tempItems[i][1]]
                        else:
                            tempList = tempItems[i][1].split('\%')
                            finalList[1] = tempList
                elif (tempItems[i][0] == 'level'):
                    if (tempItems[i][1] == ''):
                        finalList[2] = None
                    else:
                        finalList[2] = [tempItems[i][1]]
                elif (tempItems[i][0] == 'active'):
                    if (tempItems[i][1] == ''):
                        finalList[4] = None
                    else:
                        finalList[4] = tempItems[i][1]
                elif (tempItems[i][0] == 'timelim'):
                    if (tempItems[i][1] == ''):
                        finalList[5] = None
                    else:
                        finalList[5] = tempItems[i][1]
                elif (tempItems[i][0] == 'linelim'):
                    if (tempItems[i][1] == ''):
                        finalList[6] = None
                    else:
                        finalList[6] = tempItems[i][1]
                elif (tempItems[i][0] == 'conditions'):
                    if (tempItems[i][1] == ''):
                        finalList[7] = None
                    else:
                        tempConditions = tempItems[i][1].split(',')
                        tempIndividualConditions = []
                        for i in range(len(tempConditions)):
                            tempIndividualConditions.append(tempConditions[i].split('&'))
                        finalConditions = []
                        for i in range(len(tempIndividualConditions)):
                            if (len(tempIndividualConditions[i]) == 2):
                                for j in range(len(tempIndividualConditions[i])):
                                    if (len(tempIndividualConditions[i][j]) == 2):
                                        finalConditions.append([tempIndividualConditions[i][j][0],tempIndividualConditions[i][j][1]])
                            elif (len(tempIndividualConditions[i]) == 1):
                                for j in range(len(tempIndividualConditions[i])):
                                    if (len(tempIndividualConditions[i][j]) == 2):
                                        finalConditions.append([tempIndividualConditions[i][j][0],tempIndividualConditions[i][j][1]])
                        finalList[7] = finalConditions
                elif (tempItems[i][0] == 'access'):
                    if (tempItems[i][1] == ''):
                        finalList[8] = None
                    else:
                        finalList[8] = tempItems[i][1]
                elif (tempItems[i][0] == 'users'):
                    if (tempItems[i][1] == ''):
                        finalList[9] = None
                    else:
                        finalList[9] = tempItems[i][1]
            finalList[3] = userName
            return(finalList)

        def deleteCommand2(self,itemList):
            delString = itemList[3].split('-cmd:')[1]
            tempResponse = self.checkIfCommandKeyExists(delString)
            if (tempResponse == 1):
                fullDict = self.commandDictionary
                tempDict = self.commandDictionary['CMDS']
                tempSpecialSet = set(['ACTIVATINGUSER',
                                     'CHANNEL',
                                     'BOTNAME',
                                     'REMAINDER',
                                     'USERNAME',
                                     'TEMPVAL'])
                if ' ' not in delString:
                    tempInLink = tempDict[delString]['COMMAND']['LINK']
                    tempOutLinks = fullDict['LINKDICT'][tempInLink]
                    if delString not in tempSpecialSet:
                        delString = delString.lower()
                    tempResponses = []
                    tempResponseLinks = []
                    tempResponseSingularity = []
                    for item in range(len(tempOutLinks)):
                        for item2 in fullDict['LINKS']:
                            if tempOutLinks[item] in fullDict['LINKS'][item2]:
                                tempResponses.append(fullDict['LINKS'][item2][tempOutLinks[item]]['RESPONSE'])
                    for item in range(len(tempResponses)):
                        tempResponseLinks.append(fullDict['RESPONSEDICT'][tempResponses[item]])
                        if (len(tempResponseLinks[item][1]) == 1):
                            tempResponseSingularity.append(True)
                        else:
                            tempResponseSingularity.append(False)



                    if(len(tempDict[delString]) == 1):
                        del tempDict[delString]
                    else:
                        del tempDict[delString]['COMMAND']
                    del fullDict['CONDITIONS'][tempInLink]
                    del fullDict['LINKDICT'][tempInLink]
                    for item in range(len(tempResponseSingularity)):
                        if tempResponseSingularity[item]:
                            del fullDict['RESPONSEDICT'][tempResponses[item]]
                            for item4 in range(len(tempOutLinks)):
                                for item2 in fullDict['LINKS']:
                                    if tempOutLinks[item4] in fullDict['LINKS'][item2]:
                                        del fullDict['LINKS'][item2][tempOutLinks[item4]]
                            fullDict['OUTLINKS'].remove(tempOutLinks[item])
                        else:
                            fullDict['RESPONSEDICT'][tempResponses[item]][1].remove(tempInLink)
                    self.saveCommands = True
                    return [31,None]
                else:
                    delStringList = delString.split(' ')
                    tempDict2 = tempDict
                    tempCMDSList = []
                    for item in range(len(delStringList)):
                        if delStringList[item] not in tempSpecialSet:
                            delStringList[item] = delStringList[item].lower()
                        if (len(tempDict2[delStringList[item]]) == 1):
                            tempCMDSList.append(0)
                        else:
                            tempCMDSList.append(1)
                        tempDict2 = tempDict2[delStringList[item]]
                    tempCMDSBranches = tempCMDSList.count(1)
                    tempInLink = tempDict2['COMMAND']['LINK']
                    tempOutLinks = fullDict['LINKDICT'][tempInLink]
                    tempResponses = []
                    tempResponseLinks = []
                    tempResponseSingularity = []
                    for item in range(len(tempOutLinks)):
                        for item2 in fullDict['LINKS']:
                            if tempOutLinks[item] in fullDict['LINKS'][item2]:
                                tempResponses.append(fullDict['LINKS'][item2][tempOutLinks[item]]['RESPONSE'])
                    for item in range(len(tempResponses)):
                        tempResponseLinks.append(fullDict['RESPONSEDICT'][tempResponses[item]])
                        if (len(tempResponseLinks[item][1]) == 1):
                            tempResponseSingularity.append(True)
                        else:
                            tempResponseSingularity.append(False)



                    ## Start deleting multi commands
                    if (tempCMDSBranches == 0):
                        del self.commandDictionary['CMDS'][delStringList[0]]
                    else:
                        self.deleteCommandHelper(self.commandDictionary['CMDS'],tempCMDSList,delStringList,tempCMDSBranches)

                    ## Coppied from above
                    del fullDict['CONDITIONS'][tempInLink]
                    del fullDict['LINKDICT'][tempInLink]
                    for item in range(len(tempResponseSingularity)):
                        if tempResponseSingularity[item]:
                            del fullDict['RESPONSEDICT'][tempResponses[item]]
                            for item4 in range(len(tempOutLinks)):
                                for item2 in fullDict['LINKS']:
                                    if tempOutLinks[item4] in fullDict['LINKS'][item2]:
                                        del fullDict['LINKS'][item2][tempOutLinks[item4]]
                            fullDict['OUTLINKS'].remove(tempOutLinks[item])
                        else:
                            fullDict['RESPONSEDICT'][tempResponses[item]][1].remove(tempInLink)
                    self.saveCommands = True
                    return[0,None]
                return [31,None]
            else:
                return [31,None]

        def deleteCommandHelper(self, tempDict, tempCMDList, tempDelList, tempValue):
            tempCMD = tempCMDList.pop(0)
            tempDel = tempDelList.pop(0)
            if (tempCMD == 1):
                tempValue -= 1
            if (tempValue == 0):
                del tempDict[tempDel]['COMMAND']
            else:
                self.deleteCommandHelper(tempDict[tempDel],tempCMDList,tempDelList,tempValue)

        def editCommandHelper(self, tempDict, tempCMDList, tempTarget, tempValue):
            tempCMD = tempCMDList.pop(0)
            if (len(tempCMDList) < 1):
                tempDict[tempDel]['COMMAND'] = tempValue
            else:
                self.editCommandHelper(tempDict[tempDel],tempCMDList,tempValue)

        def editCommand(self, itemList):
            editString = itemList[3].split('-')[1]
            tempResponse2 = self.parseForNewCommand(itemList[3],itemList[1])
            tempResponse = self.checkIfCommandKeyExists(editString)
            if (tempResponse == 1):
                fullDict = self.commandDictionary
                tempDict = self.commandDictionary['CMDS']
                if ' ' not in delString:
                    pass
                else:
                    pass
                return 0
            else:
                return 1

        def compareForCommands(self, itemList):
            ## Make item list consist of [user groups], user name, user level,
            ## chat data, current line number, current time
            ## Need to make as part of the main class:
            ## 1. user listing of groups and levels
            ## 2. current line number
            ## 3. current time DONE
            ## 4. channel name
            ## Needs to be passed in:
            ## 1. user name
            ## 2. chat data
            tempDict = self.commandDictionary['CMDS']
            fullDict = self.commandDictionary
            tempUserName = []
            if ' ' in itemList[1]:
                pass
            else:
                ## NEED TO CONVERT USER NAMES HERE
                if itemList[1] in self.userDict:
                    tempUserName.append(itemList[1])
                    itemList[1] = 'USERNAME'
                tempSpecialSet = set(['ACTIVATINGUSER',
                                     'CHANNEL',
                                     'BOTNAME',
                                     'REMAINDER',
                                     'USERNAME',
                                     'TEMPVAL'])
                if itemList[1] not in tempSpecialSet:
                    itemList[1] = itemList[1].lower()
                try:
                    tempData = tempDict[itemList[1]]['COMMAND']
                except:
                    tempData = None
                if tempData:
                    tempOutLinks = fullDict['LINKDICT'][tempData['LINK']]
                    ## alter this later to use the conditions portion
                    ## or using chat aware selection
                    tempFinalOutLink = choice(tempOutLinks)
                    ######################################
                    ## Set user level and groups here   ##
                    try:
                        if (itemList[0] == self.botName or itemList[0] == self.boundChannel):
                            tempUserLevel = 'Owner'
                            tempUserGroups = {'owner':'0'}
                        else:
                            tempUserLevel = self.userDict[itemList[0]]['LEVEL']
                            tempUserGroups = self.userDict[itemList[0]]['GROUPS']
                        if (tempUserLevel == 'Owner'):
                            tempLevelCheck = ['owner','moderators','users']
                        elif (tempUserLevel == 'Moderator'):
                            tempLevelCheck = ['moderators','users']
                        else:
                            tempLevelCheck = ['users']
                        ######################################
                        respInfo = None
                        for item in range(len(tempLevelCheck)):
                            if not respInfo:
                                try:
                                    respInfo = fullDict['LINKS'][tempLevelCheck[item]][tempFinalOutLink]
                                    break
                                except:
                                    pass
                        self.getCurrentTime()
                        if (respInfo != None):
                            if (respInfo['LIMITS']['TIME'] == '-1' or self.currentTime > float(tempData['LASTTIME']) + float(respInfo['LIMITS']['TIME'])):
                                if (respInfo['LIMITS']['LENGTH'] == '-1' or self.currentLine > int(tempData['LASTLINE']) + int(respInfo['LIMITS']['LENGTH'])):
                                    if respInfo['GROUPS'].keys() & tempUserGroups:
                                        tempResponse = respInfo['RESPONSE']
                                        activatingUserList = ['ACTIVATINGUSER','[[user]]','[user]','@user@']
                                        channelList = ['[[channel]]','[channel]','@channel@','CHANNEL']
                                        botList = ['[[bot]]','[bot]','@bot@','BOTNAME']
                                        remainderList = ['[[remainder]]','[remainder]','@remainder@','REMAINDER']
                                        usernameList = ['[[username]]','[username]','@username@','USERNAME']
                                        for item in range(len(activatingUserList)):
                                            if activatingUserList[item] in tempResponse:
                                                tempResponse = tempResponse.replace(activatingUserList[item],itemList[0])
                                        for item in range(len(channelList)):
                                            if channelList[item] in tempResponse:
                                                tempResponse = tempResponse.replace(activatingUserList[item],self.boundChannel)
                                        for item in range(len(botList)):
                                            if botList[item] in tempResponse:
                                                tempResponse = tempResponse.replace(activatingUserList[item],self.botName)
                                        for item in range(len(usernameList)):
                                            if activatingUserList[item] in tempResponse:
                                                tempResponse = tempResponse.replace(activatingUserList[item],tempUserName[0])
                                        return([2,respInfo['RESPONSE']])

                        return [31,None]
                    except:
                        return [31,None]
                return [31,None]
            return [31,None]

        def compareHelper(self,itemList):
            pass

        ## Command Level is optional, None give all levels.
        def listCommands(self, commandLevel):
            pass

        ## Other functions. ##
        def checkChatCMD(self, chatData):
            self.currentLine += 1
            self.getCurrentTime()
            chatData[2] = self.currentTime
            if (chatData[3][:6] == 'addcom'):
                try:
                    self.makeNewEntry(self.parseForNewCommand(chatData[3],chatData[1]))
                    ##self.updateCommandDict(self.
                    return([31,None])
                except:
                    pass
            elif (chatData[3][:6] == 'delcom'):
                self.deleteCommand2(chatData)
                return([31,None])
            else:
                tempResponse = self.compareForCommands([chatData[1],chatData[3]])
                if tempResponse[1]:
                    return tempResponse
            pass

        def updateCommandDict(self, dictFileLocation):
                tempFile = open(dictFileLocation, 'w')
                tempString = json.dumps(self.commandDictionary)
                tempFile.seek(0)
                tempFile.write(tempString)
                tempFile.truncate()
                tempFile.close()

        def openCommandDictFile(self,pathName):
                tempFile = open(pathName, 'r')
                tempResponse = self.loadCommandDict(tempFile)
                tempFile.close()

        def loadCommandDict(self, dictFile):
                tempString = dictFile.read()
                self.commandDictionary = json.loads(tempString)

        def openTimerDictFile(self,pathName):
                tempFile = open(pathName, 'r+')
                self.timerDictFile = tempFile

        def updateTimerDict(self, dictFileLocation):
                tempFile = open(dictFileLocation, 'w')
                tempString = json.dumps(self.timerDictValues)
                tempFile.write(tempString)
                tempFile.close()

        def delCommandDict(self):
                self.commandDictionary = {}

        def openTwitchDictFile(self):
                tempFile = open(self.pathTwitchName, 'r')
                tempResponse = self.loadTwitchDict(tempFile)
                tempFile.close()

        def loadTwitchDict(self, dictFile):
                tempString = dictFile.read()
                dictFile.close()
                try:
                        self.twitchCommandDictionary = json.loads(tempString)
                        return 0
                except:
                        return 1

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


if __name__ == "__main__":
        from os.path import expanduser
        home = expanduser('~')
        userDict = {'SirRujak':{'GROUPS':{'default':'0'},'LEVEL':'Owner'},
                    'Avoloc':{'GROUPS':{'default':'0'},'LEVEL':'User'},
                    'Eneija':{'GROUPS':{'default':'0','talkers':'0'},'LEVEL':'Moderator'}}
        testDirectory = home + '\\Documents\\SirBotTest'
        testName = 'CoolName'
        botName = 'SirRujak'
        configFile = {'Twitch Accounts':{'automated account':{'name':botName}},'Twitch Channels':{'default channel':botName},'path':testDirectory}
        testData = [0,'SirRujak','timePlaceholder','',0,0]
        testDelete = True
        testCreate = True
        runCommandTest = True
        'addcom -cmd:hi -response:hello\%hi\%hi\&hello -level:Everyone -active:1 -linelim:-1 -timelim:-1 -conditions:>0&<2,>5&<10 -access:1 -users:group.talkers'
        eneijaTest = [['channelName','SirRujak','timePlaceholder','addcom -cmd:!tweet -response:Click to tweet out the stream! http://ctt.ec/DB4RM -level:Moderators',0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!links -response:All the things! // NomTubes // http://www.youtube.com/eneija // Tweets // http://www.twitter.com/eneija -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!patreon -response:Support in exchange for tasty rewards? Yes prease! http://www.patreon.com/eneija -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!multi -response:*insert multitwitch link* -level:Moderators -users:group.talkers SirRujak',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!panic -response:Don\'t panic guys! The stream will be fixed soon!\%CALM DOWN OR I WILL EAT YOU ALL. -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!piddleparty -response:\'Neija gotta pee! Go getchur refills and piddle to your heart\'s content! -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!uhc -response:Eneija is in the middle of an epic battle, so she might not be as responsive as usual. She still loves you though! -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!raided USERNAME -response:Thanks for the raid USERNAME ! Be sure to check out their channel: http:www.twitch.tv/USERNAME -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!raid USERNAME -response:Thanks for coming to the stream! Come raid USERNAME with me! http://www.twitch.tv/USERNAME -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!Yt -response:Ze NomTubes // http://www.youtube.com/eneija -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!twitter -response:Tasty Tweets // http://www.twitter.com/eneija -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!timeshot -response:TimeShot // http://www.reddit.com/r/TimeShot/ -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!classy -response:Let\'s keep it classy n\' sassy, friends. -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!spam -response:Please don\'t spam. It makes me hungrier. -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!banish USERNAME -response:USERNAME has been banished. -level:Moderators',0,0],

                      [0,'SirRujak','timePlaceholder','addcom -cmd:!banish2 USERNAME -response:USERNAME has been banished. -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!boop USERNAME -response:USERNAME got booped! Be nice! -level:Moderators',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd: -response: -level:Everyone',0,0],
                      [0,'SirRujak','timePlaceholder','addcom -cmd:!raid USERNAME now! -response:Thanks for coming to the stream! Come raid USERNAME with me! http://www.twitch.tv/USERNAME -level:Moderators',0,0]]
        delcomTest = [[0,'SirRujak','timePlaceholder','delcom -cmd:!tweet',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!links',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!patreon',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!multi',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!panic',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!piddleparty',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!uhc',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!raided USERNAME',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!raid USERNAME',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!yt',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!twitter',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!timeshot',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!classy',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!spam',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!banish USERNAME',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!boop USERNAME',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!banish2 USERNAME',0,0],
                      [0,'SirRujak','timePlaceholder','delcom -cmd:!raid USERNAME now!',0,0]]
        runComsTest = [[0,'Eneija',0,'!patreon',0]]
        test = ai()
        tempResponse = test.startup(configFile, userDict)
        print("Startup response: ", tempResponse)
        if testCreate:
            for i in range(len(eneijaTest)):
                    tempResponse = test.tick(eneijaTest[i])
                    if (tempResponse[0] == 1):
                        print(tempResponse)
                    test.idletick(eneijaTest[i])
        if runCommandTest:
            for item in range(len(runComsTest)):
                tempResponse = test.tick(runComsTest[item])
                if (tempResponse[0] == 1):
                    print(tempResponse)
        if testDelete:
            for i in range(len(delcomTest)):
                tempResponse = test.tick(delcomTest[i])
                if (tempResponse[0] == 1):
                    print(tempResponse)
        fullResponse = 1
        if (fullResponse != 1):
            try:
                json.dumps(test.commandDictionary, sort_keys=True, indent=4)
            except:
                print('Error converting to JSON.')
        else:
            try:
                print(json.dumps(test.commandDictionary, sort_keys=True, indent=4))
                pass
            except:
                print('Error converting to JSON.')
        test.shutdown()
        print("Done")
