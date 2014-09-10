# -*- coding: utf-8 -*-

#class for handling all data transmission over networks


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
##                        UI.terminalOutput(data)
                except:
                        logFile.write(localTime + 'Unable to send:')
                        logFile.write(messageToSend.decode() + "\r\n")
#                        print(localTime + " - Unable to send:")
#                        print(messageToSend.decode() + "\r\n")
##
                        UI.terminalOutput("Unable to send message!")
