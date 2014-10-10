# -*- coding: utf-8 -*-

#class for handling all data transmission over networks


from socket import socket,AF_INET,SOCK_STREAM,SHUT_RDWR
from urllib.request import urlopen
from queue import Queue
from time import sleep

class request():
    def __init__(self):
        pass

class stream():
    """Class for creating streaming connections, i.e., IRC threads."""
    def __init__(self):
        self.connection = socket(AF_INET,SOCK_STREAM)
        self.connection.set_inheritable(True) #we might have to do this
        self.connection.setblocking(False)
        self.inputqueue = Queue()#this could be leaving

    buffer_length = 4096

    def connect(self,host,port):
        self.connection.settimeout(5)
        self.connection.connect((host,port))
        self.connection.settimeout(0)

    def transmit(self,data):
        data = data.encode()
        self.connection.sendall(data)

    def send(self,message):
        #elevate
        if len(message) > 0:
            self.transmit(message + "\n")
            #print(message+'\n')#temporary

    def receive(self,buffer=buffer_length):
        #elevate and leave a replacement possibly without a queue
        try:
            data = self.connection.recv(buffer).decode()
        except:
            data = None
        if(data):
            for line in data.split("\n"):
                if(len(line)!=0):
                    #print(line)#temporary
                    self.inputqueue.put(line)

    def twitchConnect(self,username,token):
        #elevate
        self.connect("irc.twitch.tv",6667)#80,443
        self.send("PASS oauth:" + token)
        self.send("NICK " + username)

    def close(self):
        #elevate
        self.send("QUIT")
        self.connection.shutdown(SHUT_RDWR)
        self.connection = None

    def getInput(self):
        try:
            return(self.inputqueue.get_nowait())
        except queue.Empty:
            return(None)

    def joinTwitchChannel(self,channel):
        #elevate
        self.send("JOIN #" + channel)

    def twitchConnectv(self,username,token,retries):
        for i in range(retries):
            self.twitchConnect(username,token)
            if(self.verifyConnection(username)==True):
                break

    def verifyConnection(self,username):
        #elevate
        state = True
        motd = ['001','002','003','004','375','372','376']
        self.connection.settimeout(10)
        sleep(1)
        self.receive(350)#244+(7*len(username)))
        self.connection.settimeout(0)
        for key in range(7):
            msg = self.inputqueue.get()
            if(msg.split()[1] == 'NOTICE'):
                state = False
        return(state)

    def privmsg(self,channel,message):
        #elevate
        self.send("PRIVMSG #" + channel + ' :' + message)

    def partTwitchChannel(self,channel):
        #elevate
        self.send("PART #" + channel)

    def update(self):
        #run actions for API
        pass

    def pong(self):
        self.send("PONG")

    def chooseTwitchClient(self,choice):
        #elevate to infrasctructure or higher
        if(choice==1):
            self.send('TWITCHCLIENT 1')
        elif(choice==2):
            self.send('TWITCHCLIENT 2')
        elif(choice==3):
            self.send('TWITCHCLIENT 3')

    def clearTwitchChat(self):
        #elevate to irc or ai
        self.send('.clear')
            

if __name__ == "__main__":
    user = ''
    channel = ''
    token = ''
    x=stream()

    #sleep(.1)

    x.twitchConnect(user,token)
    print("Connection successful?",end=" ")
    print(x.verifyConnection(user))
    sleep(.25)
    x.receive()
    x.chooseTwitchClient(2)

    x.joinTwitchChannel(channel)
    #x.privmsg(channel,'wha?')
    x.receive()
    sleep(10)
    x.privmsg(channel,'oi')
    sleep(380)
    x.receive()
    x.partTwitchChannel(channel)
    sleep(5)
    x.receive()
    x.close()
    
