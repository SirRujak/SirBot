# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#### Version 0.0.8 ####
## Importing Libraries
import json
import select
import socket
import string
import time

import interface

###############################################################
###############################################################

botName = 'SirBot'
botVersion = '0.0.8'
msgID = 'Console:'
defaultState = 1

###############################################################
###############################################################


## These must currently start with ! for commands.
def checkChatCommand(channelName, chatData):
        if( chatData=="!info" ):
                message = "Watch both of us play WildStar here!: "
                return(message)
        elif( chatData[:5]=="!bop"):
                command = ".timeout " + chatData[6:] + " 30"
                return(command)
        else:
                return(checkChatStandard(chatData))


def checkChatStandard(chatData):
        if( chatData=="HAI" ):
                message = "Hello!"
                return(message)
        elif( chatData=="Nomneija, what's your favorite color?" ):
                message = "I know, I know! FOOOOOOOD! =]"
                return(message)
        else:
                return("None")


def checkChatWelcome(channelName, userName):
        #welcomeMessage = "Hello there " + userName + " welcome to the stream!"
        welcomeMessage = "A"
        return(welcomeMessage)





###############################################################
###############################################################










def sendResponse(socket, channelName, data, logFile):
        if( data == "PONG tmi.twitch.tv\r\n" ):
                socket.send(data.encode())
        else:
                messageToSend = "PRIVMSG " + channelName + " :" + data + "\r\n"
                localTime = time.asctime( time.localtime(time.time()) )
                messageToSend = messageToSend.encode()
                try:
                        
                        socket.send(messageToSend)
                        logFile.write(localTime + ' - Sent Data:')
                        logFile.write(messageToSend.decode())
#                        print(localTime + " - Sent Data:")
#                        print(messageToSend.decode() + "\r\n")
##
                        UI.terminalOutput(data)
                except:
                        logFile.write(localTime + 'Unable to send:')
                        logFile.write(messageToSend.decode() + "\r\n")
#                        print(localTime + " - Unable to send:")
#                        print(messageToSend.decode() + "\r\n")
##
                        UI.terminalOutput("Unable to send message!")
                        

def pingPong(channelName):
        pongLine = "PONG tmi.twitch.tv\r\n"
        localTime = time.asctime( time.localtime(time.time()) )
#        print(localTime + " - Sent Data:")
#        print(pongLine)
##
        UI.terminalOutput(pongLine)
        return(pongLine)

def checkChatType(channelName, chatData, modList, spamLevel, spamFilter):
        if (chatData[0]=="PING "):
                return(pingPong(channelName), 1)

        elif (len(chatData) == 2):
                chatData = chatData[1].split(" ")
                if(len(chatData) == 3):
                        if (chatData[1] == "JOIN"):
                                chatData = chatData[0].split("!")
                                chatData = chatData[0]
                                chatData = chatData[0].upper() + chatData[1:]
                                return(checkChatWelcome(channelName, chatData), 2)
                else:
                        return("None", 0)


        elif (len(chatData) > 2):
                if( chatData[2]=='The moderators of this room are' and len(chatData) > 3 ):
                        return(chatData[3], 3)
                

                if( len(chatData) == 3):
                        if( checkMods( chatData[1], modList, channelName) == 1 ):
                                chatData = chatData[2]
                                return(checkChatCommand(channelName, chatData), 1)
                        else:
                                if( checkSpam(chatData[2], spamLevel, spamFilter) == 0):
                                        chatData = chatData[2]
                                        return(checkChatStandard(chatData), 1)
                                else:
                                        testData = chatData[1].split(" ")
                                        testData = testData[0].split("!")
                                        userName = testData[0]
                                        timeOutData = ".timeout " + userName + " 30"
                                        return( timeOutData, 2 )

        else:
                return( "None", 0 )
        

def readData(socket):
        readbuffer = []
        localChatInfo = []
        try:
                readbuffer.append(socket.recv(4096).decode())
        except:
                pass
        if ( len(readbuffer) > 0 ):
                for chatItem in range(len(readbuffer)):
                        localChatInfo.extend(readbuffer[chatItem].strip().split("\n"))
        return(localChatInfo)


def checkMods(chatData, modList, channelName):
        chatData = chatData.strip().split("!")
        chatData = chatData[0]
        channelName = channelName[1:]
        if ( len(modList) > 0 ):
                if ( chatData in modList or chatData == channelName ):
                        return(1)
                else:
                        return(0)
        else:
                return(0)

def createSocket(connectionData):#PASS, NICK, IDENT, CHANNEL, HOST, PORT):
        s = socket.socket( ) ##Creating the socket variable

        s.connect((connectionData[4], connectionData[5]))##Connecting to Twitch
        Password = "PASS " + connectionData[0] + "\r\n"#PASS + "\r\n"
        s.send(Password.encode()) ##Notice how I'm sending the password BEFORE the username!

        ##Just sending the rest of the data now.
        Nickname = "Nick " + connectionData[1] + "\r\n"#NICK + "\r\n"
        s.send(Nickname.encode())
        Username = "USER " + connectionData[2] + " " + connectionData[4] + " bla :" +connectionData[1]+"\r\n"#IDENT + " " + HOST + "bla :" + REALNAME + "\r\n"
        s.send(Username.encode())

        ##Connecting to the channel.
        Channel = "JOIN " + connectionData[3] + "\r\n"
        s.send(Channel.encode() )
        s.setblocking(0) ## ensure that recv() will never block indefinitely //may eventually change
        return(s)


def checkForMods(modTimer):
        modTimer.setCurrTime(time.time())
        modTimer.checkIfTimePassed()
        if( modTimer.timePassed == 1 ):
                modTimer.prevTime = time.time()
                return( 1 )
        else:
                return( 0 )

def checkSendTimer(sendTimer):
        sendTimer.setCurrTime(time.time())
        sendTimer.checkIfTimePassed()
        if( sendTimer.timePassed == 1):
                sendTimer.prevTime =time.time()
                return( 1 )
        else:
                return( 0 )

def clearSecondarySocket(sockets, maxSockets, currSocket, channelName, logFile):
        for i in range(maxSockets+1):
                if( i != currSocket ):
##                        print("Socket " + str(i) + " cleared.")
                        chatInfo = readData(sockets[i][0][0])
                        ## Need to check for all server responses. What happens is that one of the non-current
                        ## sockets gets a response from something like .mods and then it has two in the socket
                        ## while the current only has one. This means it clears the .mods command and then
                        ## recieves the same chat data as the other just responded to making it respond twice.
                        ## Therefore if one of these is found we need to clear that socket again. Probably
                        ## need to separate the clearing and checking parts.
                        if( chatInfo[:4] == 'PING' ):
                                sendResponse(sockets[i][0][0], channelName, "PONG tmi.twitch.tv\r\n".encode(), logFile)

def getConfigInfo():
##        configFile = open('config', a)
        userName = input("Enter the twitch username your bot will use: ")
        channelName = input("Enter the channel that your bot will be on (of form #channelname): ")
        password = input("Enter the oauth password characters after 'oauth:' for connecting: ")
        socketInfo = 3
        spamLevel = input("Enter the desired spam level: ")
        spamFileName = input("Enter a file name for storing your spam data: ")
        try:
                createConfigFile(userName, channelName, password, socketInfo, spamLevel, spamFileName)
        except:
                print("Could not create a config file. Please check that you have permission.")

def createConfigFile(userName, channelName, password, socketInfo, spamLevel, spamFileName):
        configDict = {}
        configDict["CHANNEL-INFO"] = {"USERNAME":userName, "CHANNEL":channelName, "PASSWORD":password}
        configDict["SOCKET-INFO"] = {"MAX-SOCKETS":socketInfo}
        configDict["SPAM-INFO"] = {"SPAM-LEVEL":spamLevel, "SPAM-FILE-NAME":spamFileName}
#        print(configDict)
##
        UI.terminalOutput(configDict)
        configFile = open('config', 'w')
        json.dump(configDict, configFile)
        configFile.close()
        configFile = open('config', 'rb+')
        return(configFile)
##        userName = input("Enter the twitch username your bot will use: ")
##        channelName = input("Enter the channel that your bot will be on (of form #channelname): ")
##        password = input("Enter the oauth password characters after 'oauth:' for connecting: ")
##        socketInfo = 3
##        spamLevel = input("Enter the desired spam level: ")
        
def loadSpamFile(currLevel, spamFileName):
        spamFilterStuff = spamFilter(currLevel)
        spamFilterStuff.loadLevels(spamFileName)
        return(spamFilterStuff)
        
        

##def checkSpam(chatText, spamLevel):
##        if (spamLevel >= 2):
##                try:
##                        chatText.encode('ascii')
##                except:
##                        return(1)
##        if (spamLevel >= 1):
##                if ("░" in chatText
##                        or "█" in chatText
##                        or "▓" in chatText 
##                        or "▀" in chatText 
##                        or "▄" in chatText 
##                        or "▐" in chatText
##                        or "▌" in chatText
##                        or "▬" in chatText
##                        or "===" in chatText
##                        or "...." in chatText
##                        or "……" in chatText
##                        or "___" in chatText
##                        or "D~" in chatText
##                        or "┃┃" in chatText
##                        or "༼ " in chatText
##                        or "’̀-’́" in chatText
##                        or "◕" in chatText
##                        or "┌∩┐" in chatText
##                        or "_̅(" in chatText
##                        or "www" in chatText
##                        or "http" in chatText
##                        or "****" in chatText
##                        or b"\xe5\x8d\x90".decode("utf8") in chatText ):
##                        return( 1 )
##                else:
##                        return( 0 )
##        else:
##                return ( 0 )

def checkSpam(chatText, spamLevel, spamFilter):
        if (spamLevel > 21):
                spamLevel = 21
        elif (spamLevel < 0):
                spamLevel = 0
        if (spamLevel == 21):
                try:
                        chatText.encode('ascii')
                except:
                        return(1)
##        else:
        for i in range(spamLevel, 0, -1):
                tempSpamLevel = "LEVEL-" + str(i)
                if (tempSpamLevel in spamFilter.filterHolder):
                        if (chatText in spamFilter.filterHolder[tempSpamLevel]):
                                        return(1)
        return(0)
        

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
                





################################################################
##IRC connection data
def getConnectionData():
        try:
                configFile = open("config","rb+")
        except FileNotFoundError:
                configFile = getConfigInfo()
        userInfo = configFile.read().decode()
        userInfo = json.loads(userInfo)
        NICK = userInfo['CHANNEL-INFO']['USERNAME']
        IDENT = userInfo['CHANNEL-INFO']['USERNAME']
        REALNAME = userInfo['CHANNEL-INFO']['USERNAME']
        channelName = userInfo['CHANNEL-INFO']['CHANNEL']
        CHANNEL = channelName
        PASS = "oauth:" + userInfo['CHANNEL-INFO']['PASSWORD']
        HOST="irc.twitch.tv" ##This is the Twitch IRC ip, don't change it.

        PORT=6667 ##Same with this port, leave it be.
        connectionData = [PASS, NICK, IDENT, CHANNEL, HOST, PORT]
        configFile.close()
        
        return(connectionData)

def getSocketInfo():
        configFile = open("config","rb+")
        socketInfo = configFile.read().decode()
        socketInfo = json.loads(socketInfo)
        maxSockets = socketInfo['SOCKET-INFO']['MAX-SOCKETS']
        maxSockets = int(maxSockets)
        configFile.close()
        return(maxSockets)

def getSpamLevel():
        configFile = open("config","rb+")
        configInfo = configFile.read().decode()
        configInfo = json.loads(configInfo)
        spamLevel = configInfo['SPAM-INFO']['SPAM-LEVEL']
        spamFileName = configInfo['SPAM-INFO']['SPAM-FILE-NAME']
        spamLevel = int(spamLevel)
        configFile.close()
        return(spamLevel, spamFileName)

def readConfigInfo():
        connectionData = getConnectionData()
        maxSockets = getSocketInfo()
        spamLevel = getSpamLevel()
        configData = [connectionData, maxSockets, spamLevel]
        return( configData )
        



################################################################


try:
        sirLog = open('logs/SirLog.txt', 'a')
        sirLog.write('\n--------------------------------------------\n')
        sirLog.write('\nSession Start: ' + time.asctime( time.localtime(time.time()) ) + '\n' )
except:
#        print("Unable to begin logging. Please report!")
##
        UI.terminalOutput("Unable to begin logging. Please report!")
        


sessionData = getConnectionData()
channelName = sessionData[3]
(spamLevel, spamFileName) = getSpamLevel()

spamFilter = loadSpamFile(spamLevel, spamFileName)
#print(spamFilter.filterHolder)

socketReady = []

maxSocket = getSocketInfo() - 1
minSendTime = 32 / (16*(maxSocket))
for socks in range(maxSocket+1):
        socketReady.append(select.select([createSocket(getConnectionData())], [], [], 2))
##socketReady.append(select.select([createSocket(getConnectionData())], [], [], 15))
##socketReady.append(select.select([createSocket(getConnectionData())], [], [], 15))
##socketReady.append(select.select([createSocket(PASS, NICK, IDENT, CHANNEL, HOST, PORT)], [], [], 3))
currSocket = 0
##maxSocket = 1 ## one less than there actually is

####################
fastResponse = []
slowResponse = []
chatInformation = []
modList = []
modList.append(channelName[1:])
sendTimer = baseTimer(time.time(), time.time(), minSendTime)
checkModTimer = baseTimer(time.time(), time.time(), 15)
shutdownTimer = baseTimer(time.time(), time.time(), 3600)
slowResponse.append(".mods")


####################
poweredOn = 1

UI=interface.botGUI()
try:
        UI.master.iconbitmap(default='ouricon.ico')
except:
##        UI.master.tk.call('wm','iconbitmap',UI.master._w, 'ouricon.ico')
        pass
#platform specific
UI.master.title(botName + ' v.' + botVersion)
UI.owner.set(sessionData[1])
UI.channel.set(sessionData[3])

#UI.terminalOutput(str(spamFilter.filterHolder))

while( poweredOn == 1 ):

        UI.update()
        UI.update_idletasks()

        if(UI.chatStack):
                fastResponse.append(UI.chatStack.pop())
        
        if( socketReady[0][0][0] ):
                
                
                try:
                        chatInformation.extend(readData(socketReady[currSocket][0][0]))
                        clearSecondarySocket(socketReady, maxSocket, currSocket, channelName, sirLog)
                except:
                        sirLog.write(time.asctime( time.localtime(time.time()) ) + " - Unable to read data.")
#                        print(time.localtime(time.time()) + " - Unable to read data.")
##
                        UI.terminalOutput("Unable to read socket data.")

                
                if( len(chatInformation) > 0 ):
                        
                        localTime = time.asctime( time.localtime(time.time()) )
                        temp = chatInformation.pop(0)
                        temp = temp.strip('\n')
                        sirLog.write(localTime + ' - Recieved Data:')
                        try:
                                sirLog.write(temp + '\n')
                        except UnicodeEncodeError:
                                sirLog.write(localTime+"Error-Unable to encode message."+'\n')
                        temp = temp.strip().split("\n")
                        temp = temp[0].strip().split(":")
#                        print(localTime + " - Recieved Data:")
#                        print(temp)
##
                        UI.terminalInput(str(temp))
#                        print("\n")
                        try:
                                (respDat, respLev) = checkChatType(channelName, temp, modList, spamLevel, spamFilter)
                                if( respDat == "None" ):
                                        respLev = 0
                                if( respLev == 1 ):
                                        fastResponse.append(respDat)
                                elif( respLev == 2 ):
                                        slowResponse.append(respDat)
                                elif( respLev == 3 ):
                                        modList = []
                                        modList.append(channelName[1:])
                                        modList.extend(respDat)
                        except:
#                                print('\nAn error occured when checking recieved data.\n')
##
                                UI.terminalOutput("An error occured when checking received data:"+str(temp))
                                sirLog.write('\nAn error occured when checking recieved data.\n')



                ## to check and see if we need to check the mods  FIX THIS
                if( checkForMods(checkModTimer) == 1 ):
                        slowResponse.append(".mods")

                ## New timer check for sending to chat.
                if( len(fastResponse) > 0):
                        if( checkSendTimer(sendTimer) == 1 ):
                                currResponse = fastResponse.pop(0)
                                sendResponse(socketReady[currSocket][0][0], channelName, currResponse, sirLog)
                                currSocket+=1
                                if( currSocket > maxSocket ):
                                        currSocket = 0
                elif( len(slowResponse) > 0):
                        if( checkSendTimer(sendTimer) == 1 ):
                                currResponse = slowResponse.pop(0)
                                sendResponse(socketReady[currSocket][0][0], channelName, currResponse, sirLog)
                                currSocket+=1
                                if( currSocket > maxSocket ):
                                        currSocket = 0

                ## Remove for actual use, just helpful if testing times.
                shutdownTimer.setCurrTime(time.time())
                shutdownTimer.checkIfTimePassed()
                if( shutdownTimer.timePassed == 1 ):
                        poweredOn = 0
                        

                
        time.sleep(0.001)


sirLog.close()
