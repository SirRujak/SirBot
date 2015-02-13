# -*- coding: utf-8 -*-

#classes containing machinery for artifically intelligent operations
#i.e. data parsing and command execution
import json
from time import time
import queue

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
                self.timerDictFile = timerDictFile
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
                self.timerDictFile.write(tempJson)

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
        def __init__(self):
                self.boundChannel = ''
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
                self.pathTimerName = ''
                self.pathTwitchName = ''
                self.tempKeyList = []
                pass

        def startup(self, basePath, channelName):
                self.makeDictPathName(basePath, channelName) ##channelName, basePath
                try:
                        self.openCommandDictFile()
                except Exception as e:
                        return([1,e])
                try:
                        self.openTimerDictFile()
                        self.boundChannel = channelName
                        self.timerHolder = timerHolder(self,channelName,self.timerDictFile)
                        #chatHandler, channel, timerDictFile
                        self.timerHolder.startup() ##channelName, timerDictFile
                except Exception as e:
                        return([2,e])
                try:
                        self.openTwitchDictFile()
                except Exception as e:
                        return([3,e])
                return([0,None])

        def tick(self):
                self.timerHolder.tick()
                pass

        def idletick(self):
                self.timerHolder.idletick()
                pass

        def shutdown(self):
                self.timerHolder.shutdown()
                pass

        def checkChat(self, item): ## item is a list of format [type, [list with other stuff]]
                if item:
                        if (item[0] == 1):
                              pass  

        def makeDictPathName(self, basePath, channelName):
                self.pathCommandName = basePath + '//data//sirbot//commands//' + channelName + '//commands.json'
                self.pathTimerName = basePath + '//data//sirbot//timers//' + channelName + '//timers.json'
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
            splitKey = tempKey.split(' ')
            tempDict = self.commandDictionary['CMDS']
            tempVar = self.extendCheck(splitKey, tempDict)
            if (tempVar == 1):
                return 1
            else:
                return 0

        def extendCheck(self, tempList, tempDict):
            if tempList:
                tempVal = tempList.pop()
                if tempVal in tempDict:
                    tempResponse = self.extendCheck(tempList,tempDict[tempVal])
                    if (tempResponse == 1):
                        return 1
                else:
                    return 0
            else:
                return 1

        def checkIfResponseExists(self, tempResponse):
            tempList = []
            for i in range(len(tempResponse)):
                if tempResponse[i] in self.commandDictionary['RESPONSEDICT']:
                    tempList.append(self.commandDictionary['RESPONSEDICT'][tempResponse[i]])
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
            inputItems[2] = [inputItems[2][0].lower()]
            return inputItems

        def checkAllValues(self, filledEntries):
            if None in filledEntries:
                return 1
            else:
                return None
        
        ## commandLevel should be a set containing all the desired command levels
        def makeNewEntry(self,inputItems):##,commandKey,responseValue,commandLevel,
                         ##callLevel,isActive,lineLimit,timeLimit,responseLimits):
            filledEntries = self.checkForEmptySlots(inputItems)
            print(filledEntries)
            if (len(filledEntries) == 9):
                
                commandKey = inputItems[0]
                responseValue = inputItems[1]
                commandLevel = inputItems[2]
                callLevel = inputItems[3]
                isActive = inputItems[4]
                lineLimit = inputItems[5]
                timeLimit = inputItems[6]
                responseLimits = inputItems[7]
                accessLevel = inputItems[8]

                toContinue = self.checkAllValues(filledEntries)
                
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
                                self.commandDictionary["LINKS"][commandLevel[i]] = {'INFO':{'ACCESSLEVEL':accessLevel}}
                    else:
                        for i in range(len(commandLevel)):
                            self.commandDictionary["LVLS"].append(commandLevel[i])
                            self.commandDictionary["LINKS"][commandLevel[i]] = {'INFO':{'ACCESSLEVEL':accessLevel}}

                    ## Add command to the 'CMDS' dict
                    if ' ' in commandKey:
                        pass
                    else:
                        self.commandDictionary['CMDS'][commandKey] = {"LINK":str(tempInKey),
                                                                      "ACTIVE":isActive}

                    ## Add links to OUTLINKS
                    for i in range(len(tempOutKey)):
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
                        self.commandDictionary['RESPONSEDICT'][str(responseValue[i])] = str(tempOutKey[i])
                    ## Add info for LINKS
                    for i in range(len(tempOutKey)):
                        print(timeLimit,lineLimit,tempOutKey[i])
                        tempString = str(tempOutKey[i])
                        print(commandLevel)
                        self.commandDictionary['LINKS'][commandLevel[0]][tempString] = {"RESPONSE":responseValue[i],
                                                                                        "TYPE":str(tempTypeList[i]),"LIMITS":{"LENGTH":str(lineLimit),
                                                                                                                              "TIME":str(timeLimit)}}
                else:
                    return 1
                
        def parseForNewCommand(self, commandString, userName):
            tempCommandList = commandString.split(' -')
            tempItems = []
            for i in range(len(tempCommandList)):
                tempItems.append(tempCommandList[i].split(':'))
            finalList = [None]*9
            for i in range(len(tempItems)):
                if (tempItems[i][0] == 'cmd'):
                    if (tempItems[i][1] == ''):
                        finalList[0] = None
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
            finalList[3] = userName
            return(finalList)


        def deleteCommand(self, commandKey, commandLevel, callLevel):
                pass

        ## Command Level is optional, None give all levels.
        def listCommands(self, commandLevel):
                pass

        ## Other functions. ##
        def checkChatCMD(self, chatData):
                pass

        def updateCommandDict(self, dictFileLocation):
                tempFile = open(dictFileLocation, 'w')
                tempString = json.dumps(self.commandDictionary)
                tempFile.write(tempString)
                tempFile.close()

        def openCommandDictFile(self):
                tempFile = open(self.pathCommandName, 'r')
                tempResponse = self.loadCommandDict(tempFile)
        
        def loadCommandDict(self, dictFile):
                tempString = dictFile.read()
                self.commandDictionary = json.loads(tempString)
                
        def openTimerDictFile(self):
                tempFile = open(self.pathTimerName, 'r')
                self.timerDictFile = tempFile
                
        def delCommandDict(self):
                self.commandDictionary = {}

        def openTwitchDictFile(self):
                tempFile = open(self.pathTwitchName, 'r')
                tempResponse = self.loadTwitchDict(tempFile)
                tempFile.close()
                
        def loadTwitchDict(self, dictFile):
                tempString = dictFile.read()
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
        testDirectory = home + '\\Documents\\SirBotTest'
        testName = 'CoolName'
        test = chatHandler()
        tempResponse = test.startup(testDirectory, testName)
        print("Startup response: ", tempResponse)
        for i in range(10):
                test.tick()
                test.idletick()
        print("Done")
