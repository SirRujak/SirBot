# -*- coding: utf-8 -*-

#class to embody IRC elements

from time import asctime,localtime,time

class irc():
    def __init__(self,config):
        self.config = config
        self.users = {}
        self.targetchannels = []
        self.targetchannels.append(self.config['Twitch Channels']['default channel'])#temporary
        #self.sendas = self.config['

    def timeStamp(self):
        times = asctime(localtime(time()))
        times = times[11:19]
        times = '['+times+']'
        return(times)

    def styleChat(self,data):
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
        extratag = 0
        channel = None
        delimiter = ':'
        inputData.append(times)
        #message = message.rstrip('\n') #maybe necessary?
        message = message.split(' ',2)
        if(message[1] == 'PRIVMSG'):
            msgID = message[0].split('!',1)[0]
            if(msgID != ':'):
                msgID = msgID[1:]
                message = message[2].split(' ',1)
                channel = '['+message[0][1:]+']'
                message = message[1][1:]
                if(msgID == 'jtv'):
                    msgID = 'Server'
                    extratag = ['Info']
                    if(message[:9]=='USERCOLOR'):
                        msg = message.split(' ')
                        channel = ''
                        self.setUserColor(msg.pop(0),msg.pop(0))
                    elif(message[:8] == 'EMOTESET'):
                        msg = message.split(' ')
                        channel = ''
                        self.emoteHandler(msg.pop(0),msg.pop(0))
                elif(message[:11] == "\\x01ACTION"):
                    message = message.replace("\\x01ACTION",'').replace("\\x01",'')
                    delimiter = ''
                    extratag = ['Action']
            elif(msgID == ':'):
                msgID = 'Server'
                extratag = ['Info']
                message = message.split(' ',3)
                msg = message[1][1:]
                if(msg == 'SPECIALUSER'):
                    if(message[3] == 'subscriber'):
                        self.handleSubscribers(message[2])
                    elif(message[3] == 'staff'):
                        self.handleStaff(message[2])
                elif(msg == 'USERCOLOR'):
                    self.setUserColor(message[2],message[3])
                elif(msg == 'EMOTESET'):
                    self.emoteHandler(message[2],message[3])
                message = " ".join(message)
        elif(message[1] == 'JOIN'):
            msgID = 'Server'
            channel = message[2][1:]
            msg = message[0].split('!',1)[0][1:]
            message = msg + ' has joined.'
            extratag = ['Join']
            self.twitchJoin(msg,channel)
        elif(message[1] == 'PART'):
            msgID = 'Server'
            channel = message[2][1:]
            msg = message[0].split('!',1)[0][1:]
            message = msg + ' has left.'
            extratag = ['Part']
            self.twitchPart(msg,channel)
        elif(message[1] == '353'):
            msgID = 'Server'
            extratag = ['Users']
            msg = message[2].split(' ',2)
            channel = msg[1][1:]
            message = msg[2][1:]
            self.twitchUsersUpdate(message)
        elif(message[1] == '366'):
            msgID = 'Server'
            msg = message[2].split(' ',3)
            channel = msg[2][1:]
            message = msg[3][1:]
            extratag = ['Users']
        elif(message[1] == 'MODE'):
            channel = ''
            msgID = 'Server'
            extratag = ['Info']
            msg = message[2].split(' ',2)
            if(msg[1] == '+o'):
                message = 'Mods:' + msg[2]
                self.handleMods(msg[2])
            else:
                message = " ".join(msg[1:2])
        else:
            msgID = ''
            message = " ".join(message)
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
        return(message)

    def twitchJoin(self,user,channel):
        pass

    def twitchPart(self,user,channel):
        pass

    def twitchUsersUpdate(self,data):
        pass

    def setUserColor(self,user,color):
        pass

    def emoteHandler(self,user,emoteslist):
        pass

    def handleMods(self,user):
        pass

    def handleSubscribers(self,user):
        pass

    def handleStaff(self,user):
        pass
    
    def outFormat(self,message):
        #temporarily - by that i mean longterm temporarily
        return((self.targetchannels[0],message))

    def extractChat(self,message,times):
        #put message in error buffer
        inputData=[]
        extratag = 0
        inputData.append(times)
        Error = 'Error.extractChat x'
        if(message[1:4] == "'',"):
            msg = message.split("', '")
            if(len(msg) > 2):
                msg = msg[1].split(' ')[1]
                if(msg == 'PRIVMSG'):
                    msgID = str(message.split("', '")[1].split('.')[0].split('!')[0])
                    #message = ",".join(message.split(',')[2:]).strip(' ').rstrip("]").strip('"').strip("'")
                    message = ",".join(message.split(',')[2:])[2:][:-2]
                    if(msgID == 'jtv'):
                        msgID = 'Server'
                        extratag=['Info']
                        if(message.split(' ')[0]=="USERCOLOR"):
                            self.addColor(message.split(' ')[2])
                elif(msg in ['001','002','003','004','375','372','376']):
                    msgID = 'Server'
                    message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    extratag = ['Welcome']
                elif(msg == '353'):
                    msgID = 'Server'
                    #self.userlisterror.append(message)
                    #self.messagelen.append(len(message))
                    #self.extractUsers(len(message))
                    message =  ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    self.extractUsers(message)
                    message = 'USERS-' + message
                    extratag = ['Users']
                elif(msg == '366'):
                    #self.userlisterror.clear()
                    self.checkUserMultiplicity()
                    message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    msgID = 'Server'
                    extratag=['Users']
                else:
                    msgID = ''
                    extratag = ['Error']
                    #self.chatError(msg,msgID,message)
                    #self.userlisterror.append(message)
            elif(len(msg) == 2):
                if(len(msg[1].split(' '))>=2):
                    msg=msg[1].split(' ')[1]
                    if(msg == 'PART'):
                        msgID = 'Server'
                        message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                        self.partUsers(message)
                        message = message + " has left."
                        extratag = ['Part']
                    elif(msg == 'JOIN'):
                        msgID = 'Server'
                        message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                        self.joinUsers(message)
                        message = message + " has joined."
                        extratag = ['Join']
                    elif(msg=='353'):
                        msgID='Server'
                        extratag = ['Error']
                        #self.userlisterror.append(message)
                    elif(msg == 'MODE'):
                        #potentially other options besides +o to account for here someday - not too sure here
                        msgID = 'Server'
                        message = "".join(message.split("', '")[1][9:]).strip(']').strip("'")
                        if(message.split(' ')[1] == '+o'):
                            message = 'Mods:' + " ".join(message.split(' ')[2:])
                            extratag = ['Mods']
                        else:
                            extratag = ['Error']
                    elif(msg == 'PRIVMSG'):
                        try:
                            msgID = message.split("', '")[1].split('.')[0].split('!')[0]
                            #message = ",".join(message.split(',')[2:]).strip(' ').rstrip("]").strip("'").strip('"')
                            message = ",".join(message.split(',')[2:])[2:][:-2]
                        except:
                            msgID = 'PRIVMSG'
                            extratag = ['Error']
                        #self.chatError(msg,msgID,message)
                    else:
                        msgID = ''
                        #self.chatError(msg,msgID,message)
                        extratag = ['Error']
                else:
                    msgID = ''
                    #self.chatError('',msgID,message)
                    extratag = ['Error']
            else:
                msg = msg[1].split(' ')[1]
                msgID = ''
                #self.chatError(msg,msgID,message)
                extratag = ['Error']
        elif(message[1:8] == "'PING '"):
            if(message[11:24] == "tmi.twitch.tv"):
                msgID = 'Server'
                message = 'PING! '
                extratag = ['Ping']
            else:
                msgID = 'Server'
                self.chatError('',msgID,message)
                extratag = ['Ping','Error']
        else:
            #further contingencies go here someday
            msgID = ''
            #if(self.userlisterror):
                #self.userlisterror.append(message)
                #(fixable,temp) = self.fixUserList(message)
                #if(fixable):
                    #message = temp
                    #return('Server:',temp.strip("[']"))
                #else:
                    #self.chatError('',msgID,message)
            #else:
                #self.chatError('',msgID,message)
            #return(msgID,(Error +"003: -"+message))
            extratag = ['Error']

        inputData.append(msgID)
        inputData.append(': ')
        inputData.append(message)
        inputData.append(extratag)

        return(inputData)
    
    def chatError(self,data):
        #message recovery tool
        pass

    def extractUsers(self,message):
        self.using.extend(message.split(' '))
        self.setUsers()

    def joinUsers(self,user):
        try:
            self.using.append(user)
            self.setUsers()
        except:
            pass

    def partUsers(self,user):
        try:
            self.using.remove(user)
            self.setUsers()
        except:
            pass

    def formatUserList(self):
        #self.users
        #insert headings for various tiers
        pass

    def fixUserList(self,message):
        fixable = False
        while(len(self.userlisterror)>2):
            self.userlisterror.pop(0)
        if(len(self.userlisterror)==2):
            if(self.userlisterror[1].find(',')==-1 and self.userlisterror[0].split("', '")[1].split(' ')[1]=='353'):
                message = self.userlisterror[0].split("', '")[2].strip(']').strip("'").split(' ')
                message = message[len(message)-1]
                try:
                    self.using.remove(message)
                    self.setUsers()
                    
                except:
                    #this should never happen, but need to make note somehow if it does
                    pass
                message = message + self.userlisterror[1].lstrip('[').rstrip(']').strip("'")
                message = "Recovered:NAMES-" + message
                fixable = True
                self.userlisterror.clear()
            else:
                message = self.userlisterror[0][:len(self.userlisterror[0])-2]+self.userlisterror[1][2:]
                tag = message.split("', '")[1].split(' ')[1]
                if(tag=='353'):
                    message = "Recovered:NAMES-" + message
                    fixable = True
                    self.userlisterror.clear()
                else:
                    message=self.userlisterror.pop(0)
                    self.chatError('','',message)
        else:
            pass
        self.checkUserMultiplicity()
        return(fixable,message)

    def checkUserMultiplicity(self):
        #check how many times each user appears in self.using; update self.users
        #make note in log of occurance
        #temporarily print out names that have multiplicities
#        print('Coming soon...')
        for _user in self.using:
            while(True):
                try:
                    index=self.using.index(_user,self.using.index(_user)+1)
                    self.using.pop(index)
                    #print(self.using.pop(index))

                except ValueError:
                    break
                except:
                    #unexpected error needs to be logged
                    break

        self.setUsers()



#tags:
#input/*username*/server/console
#time/text

#/join/part/welcome/users/ping/mods/info/error/recovered/raw

#['<timestamp>','<input/*username*/server/console>',':','<message>',[<extra-tags>]]
