# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#### Version 0.0.7 ####
##Socket library
import json
import select
import socket
import string
import time




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
        welcomeMessage = "Hello there " + userName + " welcome to the stream!"
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
                        print(localTime + " - Sent Data:")
                        print(messageToSend.decode() + "\r\n")
                except:
                        logFile.write(localTime + 'Unable to send:')
                        logFile.write(messageToSend.decode() + "\r\n")
                        print(localTime + " - Unable to send:")
                        print(messageToSend.decode() + "\r\n")
                        

def pingPong(channelName):
        pongLine = "PONG tmi.twitch.tv\r\n"
        localTime = time.asctime( time.localtime(time.time()) )
        print(localTime + " - Sent Data:")
        print(pongLine)
        return(pongLine)

def checkChatType(channelName, chatData, modList):
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
                                if( checkSpam(chatData[2]) == 0):
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

def checkSpam(chatText):
        if ("░" in chatText
                or "█" in chatText
                or "▓" in chatText 
		or "▀" in chatText 
		or "▄" in chatText 
		or "▐" in chatText
		or "▌" in chatText
                or "▬" in chatText
		or "===" in chatText
		or "...." in chatText
                or "……" in chatText
                or "___" in chatText
                or "D~" in chatText
                or "┃┃" in chatText
                or "༼ " in chatText
                or "’̀-’́" in chatText
                or "◕" in chatText
                or "┌∩┐" in chatText
                or "_̅(" in chatText
                or "www" in chatText
                or "http" in chatText
		or b"\xe5\x8d\x90".decode("utf8") in chatText ):
                return( 1 )
        else:
                return( 0 )

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





################################################################
##IRC connection data
def getConnectionData():
        configFile = open("config","rb+")
        userInfo = configFile.read().decode()
        userInfo = json.loads(userInfo)
        NICK = userInfo['USERNAME']
        IDENT = userInfo['USERNAME']
        REALNAME = userInfo['USERNAME']
        channelName = userInfo['CHANNEL']
        CHANNEL = channelName
        PASS = "oauth:" + userInfo['PASSWORD']
        HOST="irc.twitch.tv" ##This is the Twitch IRC ip, don't change it.

        PORT=6667 ##Same with this port, leave it be.
        connectionData = [PASS, NICK, IDENT, CHANNEL, HOST, PORT]
        configFile.close()
        
        return(connectionData)



################################################################


try:
        sirLog = open('logs/SirLog.txt', 'a')
        sirLog.write('\n--------------------------------------------\n')
        sirLog.write('\nSession Start: ' + time.asctime( time.localtime(time.time()) ) + '\n' )
except:
        print("Unable to begin logging. Please report!")


channelName = getConnectionData()[3]

socketReady = []
socketReady.append(select.select([createSocket(getConnectionData())], [], [], 15))
##socketReady.append(select.select([createSocket(getConnectionData())], [], [], 15))
##socketReady.append(select.select([createSocket(PASS, NICK, IDENT, CHANNEL, HOST, PORT)], [], [], 3))
currSocket = 0
maxSocket = 0

####################
fastResponse = []
slowResponse = []
chatInformation = []
modList = []
modList.append(channelName[1:])
sendTimer = baseTimer(time.time(), time.time(), 0.05)
checkModTimer = baseTimer(time.time(), time.time(), 15)
shutdownTimer = baseTimer(time.time(), time.time(), 20)
slowResponse.append(".mods")


####################
poweredOn = 1
while( poweredOn == 1 ):
        if( socketReady[0][0][0] ):
                
                try:
                        chatInformation.extend(readData(socketReady[0][0][0]))
                except:
                        sirLog.write(time.asctime( time.localtime(time.time()) ) + " - Unable to read data.")
                        print(time.localtime(time.time()) + " - Unable to read data.")
                
                if( len(chatInformation) > 0 ):
                        
                        localTime = time.asctime( time.localtime(time.time()) )
                        temp = chatInformation.pop(0)
                        temp = temp.strip('\n')
                        sirLog.write(localTime + ' - Recieved Data:')
                        sirLog.write(temp + '\n')
                        temp = temp.strip().split("\n")
                        temp = temp[0].strip().split(":")
                        print(localTime + " - Recieved Data:")
                        print(temp)
                        print("\n")
                        try:
                                (respDat, respLev) = checkChatType(channelName, temp, modList)
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
                                print('\nAn error occured when checking recieved data.\n')
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
                        

                
        time.sleep(0.075)


sirLog.close()