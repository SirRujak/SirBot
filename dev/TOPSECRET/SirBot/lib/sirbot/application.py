# -*- coding: utf-8 -*-

#wrapper for applications elements

#NOTE:this has permission to change config - NOTHING ELSE has permission(virtual)

from lib.sirbot.irc import irc

from time import sleep, time

from queue import Empty

from lib.sirbot.network import stream, secureStream

from lib.sirbot.web import twitch

class application():
    def __init__(self,config,interinput = None,interoutput = None):
        #things will be selectively loaded based on choices in config
        self.allocateVars(config,interinput,interoutput)

    def begin(self):#this is just temporary until proper controls can be created in GUI
        self.createModules()
        #self.automatedIRC.chooseTwitchClient(2)
        if(self.config['Twitch Channels']['default channel'] != 0):
            self.joinATwitchChannel(self.config['Twitch Channels']['default channel'])
        if(self.config['Twitch Automated Moderator']['watch for followers']):
            self.twitchDataSource.twitchconnect()

    def createModules(self):
        self.createIRCclient()
        self.createIRCstreams('twitch')
        self.createDataStreams()
        self.twitchWeb = twitch(self.config['Twitch Channels']['default channel'])


    def allocateVars(self,config,interinput,interoutput):
        self.idletime = 0
        self.config = config
        self.interinput = interinput
        self.interoutput = interoutput
        self.status = 1 #1 to continue running, 0 to terminate
        self.input = []
        self.output = []
        self.streams = []
        self.chatcache = []
        self.chatcache.append(self.config['Interface']['motd'])

    def shutdown(self):
        #save all data from queues to file and close module
        pass

    def tick(self):
        #update tick to perform operations each iteration
        self.intakeData()
        self.processData()
        self.outputData()
        sleep(0.001)
        return(self.status)

    def outputData(self):
        #sends processed data on it's way
        for item in self.output:
            """ OUTPUT CODES:
            0-10=outbound internet data
            --2=automated irc account stream chat
            --3=trusted irc account stream chat
            --7=web.py twitch.tv requests
            11-20=internal data
            --17=web.py twitch follower notices
            21-30=interface data
            --24=irc chat messages
            --25=interface configurations (interface to app)
            --26=interface data (app to interface)
            31-99=overflow internal data
            """
            if(item[0]<=10):
                if(item[0]==2):
                    self.automatedIRC.privmsg(item[1][0],item[1][1])#needs to be .privmsg with channel
                elif(item[0]==3):
                    self.trustedIRC.privmsg(item[1][0],item[1][1])#item[1] = (channel,message)
                elif(item[0]==4):
                    self.twitchDataSource.transmit(item[1])
                elif(item[0]==7):
                    self.twitchWeb.inputqueue.put(item)
            elif(item[0]<=20):
                #internal data - mostly ai.py
                pass
            elif(item[0]<=30):
                if(item[0]==24):
                    try:
                        self.interinput.put(item)
                    except AttributeError:
                        pass
                elif(item[0]==25):
                    try:
                        self.interinput.put(item)
                    except AttributeError:
                        pass
                elif(item[0]==26):
                    #print(item)
                    try:
                        self.interinput.put(item)
                        #print(item)
                    except AttributeError:
                        pass
            else:
                pass
            self.output = []
            
    def intakeData(self):
        #check all data input
        if(self.config['GUI']==1):
            self.checkInterface()
        self.checkNetwork()
        self.checkModules()

    def processData(self):
        #perform operations on data using imported modules
        #for now just irc
        #retrieve incoming data from self.input
        #deposit outgoing data into self.output

        #module ticks
        self.twitchWeb.tick()

        #idle chat check - for pings mostly
        if(time()-self.idletime > 15):
            try:
                message = self.chatcache.pop()
                if(message[0]==':'):
                    self.chat.inFormat(message,self.chat.timeStamp())
                elif(message[0]=='P'):
                    self.chat.inFormatPING(message,self.chat.timeStamp())
                    self.sendPong()
                else:
                    self.chatcache.append(message)
            except IndexError:
                pass
            self.idletime = time()
        
        for item in self.input:
            if(item[0]==10):
                if(item[1][0]==':'):
                    if(self.config['Interface']['chat']['raw']!=1):
                        try:
                            self.output.append([24,
                                                self.chat.inFormat(self.chatcache.pop(),
                                                                   self.chat.timeStamp())])
                        except IndexError:
                            self.chatcache.append(item[1])
                            self.idletime = time()
                    else:
                        self.output.append([24,self.chatcache.pop()])
                #self.chatcache.append(item[1])
                elif(item[1][:19] == "PING :tmi.twitch.tv"):#change to inFormatPING(
                    self.output.append([24,self.chat.inFormatPING(item[1],self.chat.timeStamp())])
                    self.sendPong()
                    print(True)
                else:
                    fragment = self.chatcache.pop()
                    self.chatcache.append(fragment+item[1])
            elif(item[0]==2):
                self.output.append([2,self.chat.outFormat(item.pop())])
            elif(item[0]==3):
                self.output.append([3,self.chat.outFormat(item.pop())])
            elif(item[0]==4):
                self.output.append(item)
            elif(item[0]==7):
                self.output.append(item)
            elif(item[0]==25):
                self.applySettings(item[1])
                self.output.append(item)
            elif(item[0] == 26):
                self.output.append(item)
        self.input = []
                
    def closeApplication(self):
        self.status = 0
        for element in self.IRCstreams:
            element.close()

    def applySettings(self,data):
        #apply settings to application or update config
        if(data == 0):
            self.status = 0
    
    def sendPong(self):
        #consider elevating to IRC.py?
        self.automatedIRC.pong()
        if(self.config['Twitch Accounts']['trusted account']['join chat']==1):
            self.trustedIRC.pong()
     
    def createIRCclient(self):
        self.chat = irc(self.config)

    def createIRCstreams(self,selection):
        retries = self.config['MISC']['twitch connect retries']
        if(selection.lower() == 'twitch'):
            self.automatedIRC = stream()
            self.automatedIRC.twitchConnectv(self.config['Twitch Accounts']
                                                  ['automated account']
                                                  ['name'],
                                                  self.config['Twitch Accounts']
                                                  ['automated account']
                                                  ['token'],retries)
            self.IRCstreams = [self.automatedIRC]
            if(self.config['Twitch Accounts']['trusted account']['token'] != 0):
                self.trustedIRC = stream()
                self.trustedIRC.twitchConnectv(self.config['Twitch Accounts']
                                                    ['trusted account']
                                                    ['name'],
                                                    self.config['Twitch Accounts']
                                                    ['automated account']
                                                    ['token'],retries)
                self.IRCstreams.append(self.trustedIRC)
        self.streams.extend(self.IRCstreams)

    def createDataStreams(self):
        if(self.config['Twitch Automated Moderator']['watch for followers']):
            self.twitchDataSource = secureStream()
            self.DataSources = [self.twitchDataSource]
    def checkInterface(self):
        #get from interface input queue
        #could grab more items here at some point
        try:
            temp = self.interoutput.get_nowait()
            self.input.append(temp)
            #print(temp)
        except Empty:
            pass
        except AttributeError:
            pass

    def checkNetwork(self):
        #get incoming data from all network connections
        #could grab more items here at some point
        for element in self.streams:
            try:
                element.receive()
                temp = element.inputqueue.get_nowait()
                self.input.append(temp)
                #print(temp)
                temp = None
            except Empty:
                pass
        for element in self.DataSources:
            data = element.receive()
            if(data):
                self.input.append([7,data])
                
    def joinATwitchChannel(self,channel):
        self.automatedIRC.joinTwitchChannel(channel)
        if(self.config['Twitch Accounts']['trusted account']['join chat']!=0):
            self.trustedIRC.joinTwitchChannel(channel)

    def checkModules(self):
        try:
            temp = self.chat.outputqueue.get_nowait()
            self.input.append(temp)
            #print(temp)
        except Empty:
            pass

        try:
            temp = self.twitchWeb.outputqueue.get_nowait()
            self.input.append(temp)
        except Empty:
            pass

        try:
            temp = self.twitchWeb.outputqueue.get_nowait()
            self.input.append(temp)
        except Empty:
            pass
        
    
    #channel,timestamp,sender,message
