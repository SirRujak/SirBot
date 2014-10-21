# -*- coding: utf-8 -*-

#class to embody IRC elements

from time import asctime,localtime,time
from queue import Queue

class irc():
    def __init__(self,config):
        self.config = config
        self.users = {}
        self.channels = []
        self.groups = []
        self.groups.append('ADMINISTRATORS')#temporary - eventually needs to come from config
        self.groups.append('MODS')
        self.outputqueue = Queue()
        self.channels.append(self.config['Twitch Channels']['default channel'])#temporary
        #self.sendas = self.config[' ??

    def timeStamp(self):
        times = asctime(localtime(time()))
        times = times[11:19]
        times = '['+times+']'
        return(times)

    def styleChat(self,data):
        #deprecated
        #consider implementing a tag for actions- would need low priority
        if(data[1] is not 'Server'):
            data[3] = data[3].replace("\\'","'")
            data[3] = data[3].replace("', '",":")
            data[3] = data[3].replace('", "',":")
            data[3] = data[3].replace('''', "''',":")
            data[3] = data[3].replace("""", '""",":")
            if("\\x01ACTION" in data[3]):
                data[3] = data[3].replace("\\x01ACTION",'')
                data[3] = data[3].replace("\\x01",'')
                data[2] = ''
        return(data)

    def inFormat(self,message,times):
        inputData = []
        cache = message
        extratag = 0
        channel = None
        delimiter = ':'
        inputData.append(times)
        message = message.split(' ',2)
        if(message[1] == 'PRIVMSG'):
            msgID = message[0].split('!',1)[0][1:]
            if(msgID != 'jtv'):
                message = message[2].split(' ',1)
                channel = '['+message[0][1:]+']'
                message = message[1][1:]
                if(str(message[:7]) == "\x01ACTION"):
                    message = str(message).replace("\x01ACTION",'').replace("\x01",'')
                    delimiter = ''
                    extratag = ['Action']
            elif(msgID == 'jtv'):
                channel = ''
                msgID = 'Server'
                extratag = ['Info']
                message = message[2].split(' ',1)[1]
                msg = message.split(' ',1)[0][1:]
                if(msg == 'SPECIALUSER'):
                    if(message[3] == 'subscriber'):
                        self.handleSubscribers(message[2])
                    elif(message[3] == 'staff'):
                        self.handleStaff(message[2])
                    message = message[1:]
                elif(msg == 'USERCOLOR'):
                    self.setUserColor(message[2],message[3])
                    message = message[1:]
                elif(msg == 'EMOTESET'):
                    self.emoteHandler(message[2],message[3])
                    message = message[1:]
                elif(msg == 'HISTORYEND'):
                    message = message[1:]
##                elif(msg == 'The'):
##                    #this doesn't contain the channel, will need to take some time on this.
##                    if(message[:34] == ':The moderators of this room are: '):
##                        pass
                else:
                    msgID = ''
                    delimiter = ''
                    extratag = ['Error']
                    message = cache
        elif(message[1] == 'JOIN'):
            msgID = 'Server'
            chann = message[2][1:]
            channel = '[' + chann + ']'
            msg = message[0].split('!',1)[0][1:]
            message = msg + ' has joined.'
            extratag = ['Join','Info']
            self.twitchJoin(msg,chann)
        elif(message[1] == 'PART'):
            msgID = 'Server'
            chann = message[2][1:]
            channel = '[' + chann + ']'
            msg = message[0].split('!',1)[0][1:]
            message = msg + ' has left.'
            extratag = ['Part','Info']
            self.twitchPart(msg,chann)
        elif(message[1] == '353'):
            msgID = 'Server'
            extratag = ['Users','Info']
            msg = message[2].split(' ',3)
            chann = msg[2][1:]
            channel = '[' + chann + ']'
            message = msg[3][1:]
            self.twitchUsersUpdate(chann,message)
            message = 'USERS- ' + message
        elif(message[1] == '366'):
            msgID = 'Server'
            msg = message[2].split(' ',2)
            chann = msg[1][1:]
            channel = '[' + chann + ']'
            message = msg[2][1:]
            extratag = ['Users','Info']
            self.twitchUsersUpdate(chann)
        elif(message[1] == 'MODE'):
            msgID = 'Server'
            extratag = ['Info']
            msg = message[2].split(' ',2)
            chann = msg[0][1:]
            channel = '{' + chann + ']'
            if(msg[1] == '+o'):
                message = '-MODS- ' + msg[2]
                self.handleMods(chann,msg[2])
            else:
                msgID = ''
                delimiter = ''
                channel = ''
                message = cache
                extratag = ['Error']
        else:
            msgID = ''
            message = cache
            delimiter = ''
            channel = ''
            if(message != self.config['Interface']['motd']):
                extratag = ["Error"]

        inputData.append(channel)
        inputData.append(msgID)
        inputData.append(delimiter)
        inputData.append(message)
        inputData.append(extratag)
        
        return(inputData)

    def inFormatPING(self,message,times):
        #temporary
        inputData = [times,'','Server',':',message,['Ping','Info']]
        return(inputData)

    def twitchJoin(self,user,channel):
        if(channel in self.users):
            self.users[channel][user] = {}
        else:
            self.users[channel]={}
            self.users[channel][user]={}
        self.groupAdministrator(channel,user)
        self.twitchUsersUpdate(channel)#<-need to run this at intervals, not here

    def twitchPart(self,user,channel):
        try:
            if(channel in self.users):
                if(user in self.users[channel]):
                    del self.users[channel][user]
            self.twitchUsersUpdate(channel)
        except KeyError:
            pass

    def twitchUsersUpdate(self,channel=None,data=None):
        if(data):
            if(channel not in self.users):
                #add strings to dictionary
                self.users[channel] = {}
            for user in data.split(' '):
                self.users[channel][user] = {}
                self.groupAdministrator(channel,user)
        else:
            #add case for when given a channel
            userlist = self.sortUsers()#<-preferrably run this
            self.outputqueue.put([26,['users',userlist]])

    def sortUsers(self):
        #sorts users. takes either list or dict
        if(self.config['Interface']['user list']['show channels']==1):
            userlist = []
            #format things
            for achannel in self.channels:
                channellist = self.groupUsers(achannel)
                if(channellist):
                    userlist.append('#'+achannel)
                    userlist.extend(channellist)
        else:
            userlist = self.groupUsers()
        return(userlist)

    def groupUsers(self,achannel=None):
        channellist = []
        if(self.config['Interface']['user list']['show groups']==1):
            users = set()
            if(achannel):
                for agroup in self.groups:
                    grouplist = []
                    for user in self.users[achannel]:
                        if(self.users[achannel][user]):
                            if(agroup in self.users[achannel][user]):
                                grouplist.append(user)
                        else:
                            users.add(user)
                    if(grouplist):
                        grouplist = self.orderUsers(grouplist)
                        channellist.append("--"+agroup+"--")
                        channellist.extend(grouplist)
                if(users):
                    using = self.orderUsers(users)
                    channellist.append("--USERS--")
                    channellist.extend(using)
            else:
                for agroup in self.groups:
                    grouplist = []
                    for achannel in self.channels:
                        for user in self.users[achannel]:
                            if(self.users[achannel][user]):
                                if(agroup in user):
                                    grouplist.append(user)
                            else:
                                users.add(user)
                        if(grouplist):
                            grouplist = self.orderUsers(grouplist)
                            channellist.append("--" + agroup + "--")
                            channellist.extend(grouplist)
                if(users):
                    using = self.orderUsers(users)
                    channellist.append("--USERS--")
                    channellist.extend(using)
        else:
            if(achannel):
                channellist = list(self.users[achannel])
                channellist = self.orderUsers(channellist)
            else:
                for achannel in self.channels:
                    achannellist = list(self.users[achannel])
                    channellist.extend(achannellist)
                channellist = self.orderUsers(channellist)
        return(channellist)
           

    def orderUsers(self,data):
        #takes a list/set of users and returns an equivalent, ordered list
        #currently only capable of alphabetization - TO BE EXTENDED
        if(self.config['Interface']['user list']['sort']=='alpha'):
            data = sorted(data)
        return(data)

    def groupAdministrator(self,channel,user):
        #add group attributes to members
        #if(user==self.config['Twitch Accounts']['automated account']['name']):
        #    self.users[channel][user]['Administrators'] = 1
        #elif(user==self.config['Twitch Accounts']['trusted account']['name']):
        #    self.users[channel][user]['Administrators'] = 1
        if(user==channel):
            self.users[channel][user]['ADMINISTRATORS'] = 1
        #need records of user groups per channel to check here

    def setUserColor(self,user,color):
        pass

    def emoteHandler(self,user,emoteslist):
        pass

    def handleMods(self,channel,user):
        try:
            self.users[channel][user]['MODS'] = 1
        except KeyError:
            try:
                self.users[channel][user] = {}
                self.users[channel][user]['MODS'] = 1
            except KeyError:
                self.users[channel] = {}
                self.users[channel][user] = {}
                self.users[channel][user]['MODS'] = 1
        self.twitchUsersUpdate()
            
            

    def handleSubscribers(self,user):
        pass

    def handleStaff(self,user):
        pass
    
    def outFormat(self,message):
        #temporarily - by that i mean longterm temporarily
        return((self.channels[0],message))



##NOTES:

#tags:
#input/*username*/server/console
#time/text

#/join/part/welcome/users/ping/mods/info/error/recovered/raw

#['<timestamp>','<input/*username*/server/console>',':','<message>',[<extra-tags>]]
