# -*- coding: utf-8 -*-

#class for interfacing with twitch.tv

#######################################################
#  need to extract requests and sync with network.py  #
#######################################################

from urllib.request import urlopen #want this out of here

from json import loads
from queue import Queue,Empty
from time import time

class twitch():
    def __init__(self,user):
        self.initialized = 0
        self.state = 0
        self.inputqueue = Queue()
        self.outputqueue = Queue()
        self.cache = Queue()
        self.workingstack = []
        self.channels = {}
        self.addChannel(user)
        self.followers = []
        self.newFollowers = []
        self.numberFollowers = None
        self.latestFollower = None
        #self.getInitialFollowerInfo()#uh oh
        #self.getInitialLatestFollowers()#double uh oh
        self.streamData = None
        #self.numberSubscriber = 
        #self.latestSubscriber =

    def getFollowersInfo(self):
        url = 'https://api.twitch.tv/kraken/channels/'+self.user+'/follows?limit=10'
        self.outputqueue.put([7,[1,url]])

    def tick(self):
        if(self.state==0):
            self.request()
        elif(self.state==1):
            self.intake()
        elif(self.state==2):
            self.prepare()
        elif(self.state==3):
            self.check()
        elif(self.state==4):
            self.notify()
        #self.newFollowers(self.user)

    def update(self):
        #get latest channel status/etc.
        self.intakeData()
        #self.requestStreamData(self.user)#

    def addChannel(self,channel):
        self.channels[channel]=[int(0),int(0)]
    
    def newFollowers(self,user):
        followers = self.getLatestFollower(user)
        numfollowers = self.getFollowerCount(user)
        if(self.latestFollower == followers):
            if(self.numberFollowers==numfollowers):
                #no changes
                pass
            else:
                #this is the tricky one
                #need to check created_at values
                pass
        else:
            #probably have a new follower
            if(self.numberFollowers<numfollowers):
                newusers = self.getLatestFollowers(self.user,numfollowers-self.numberFollowers)
                if(newusers[0]==self.latestFollower):
                    self.output([14,newusers[1:]])
                    self.latestFollower = newusers[-1]
            else:
                #could also be tricky
                #some followers have left
                #but may have new ones
                pass

    def requestFollowerData(self,user,limit='5'):
        request = "GET /kraken/channels/" + user
        request = request + "/follows?limit=" + limit
        request = request + " HTTP/1.1\r\nHost: api.twitch.tv\r\n\r\n"
        self.outputqueue.put([4,request])

    def requestStreamData(self,user):
        #get stream status/info
        request = "GET /kraken/streams/" + user
        request = request + " HTTP/1.1\r\nHost: api.twitch.tv\r\n\r\n"
        self.outputqueue.put([4,request])

    def intakeData(self):
        #take data from inputqueue
        try:
            data = self.inputqueue.get_nowait()
        except Empty:
            pass

    def request(self):
        #request either follower/subscriber/stream data based on time elapsed
        for channel in self.channels:
            now = time()
            if(now - self.channels[channel][0] > 30):
                self.channels[channel][0] = now
                self.requestStreamData(channel)
                self.state = 1
            elif(now - self.channels[channel][1] > 15):
                self.channels[channel][1] = now
                self.requestFollowerData(channel)
                self.state = 1
                

    def intake(self):
        #take data from inputqueue if time differential is great enough
        try:
            data = self.inputqueue.get_nowait()
        except Empty:
            pass
        else:
            self.workingstack.append(data)
            self.state = 2

    def prepare(self):
        #prepare input for processing
        data = self.workingstack.pop()
        data = data[1]
        data = data.split("\r\n\r\n")
        data = data[1]
        data = data.split('\r\n')
        try:
            data = data[1]
        except IndexError:
            data = data[0]
        try:
            data = loads(data)
        except ValueError:
            self.state = 0
        else:
            self.workingstack.append(data)
            self.state = 3

    def check(self):
        #process input
        data = self.workingstack.pop()
        try:
            newlist = []
            for item in data["follows"]:
                newlist.append(item["user"]["display_name"])
            
        except KeyError:
            try:
                item = data["stream"]#not finished
                self.state = 0
            except KeyError:
                self.state = 0
                #not finished

        else:
            #may need to trim followers list at some point
            for user in newlist:
                if user in self.followers:
                    pass
                else:
                    self.followers.append(user)
                    self.newFollowers.append(user)
            if(self.newFollowers):
                self.state = 4
            else:
                self.state = 0

    def notify(self):
        #notify streamer of new follower
        if(self.initialized == 1):
            for user in self.newFollowers:
                self.newFollowerMessage(user)
        else:
            self.initialized = 1
        self.newFollowers = []
        self.state = 0

    def newFollowerMessage(self,user):
        #send notification for new follower to chat
        self.outputqueue.put([2,user+" has been assimilated. Resistance is futile."])
            

    def sortData(self,data):
        #sort data pulled from queue
        #should be a list where first entry is an identifier code
        #if(data[0]==#... etc.
        #then create different functions for different types of data
        #need id code for streamData,followerdata,
        #if(data[0]==7):
            #self.createJSONobject(data[1])
        pass

    def getStreamInfo(self,userName):
        #deprecated
        errFlag = 0
        try:
            try:
                url = 'https://api.twitch.tv/kraken/streams/' + userName
            except TypeError:
                url = 'https://api.twitch.tv/kraken/streams/' + str(userName)
            streamData = urlopen(url)
            streamData = streamData.read()

        except:
            errFlag = 1
            streamData = 0

        return(streamData,errFlag)


    def getTwitchState(self,streamData):
        errFlag = 0
        try:
            streamData = loads(streamData.decode())
            isStreaming = streamData['stream']
            if(isStreaming!=None):
                isStreaming = 'true'
            else:
                isStreaming = 'false'

        except:
            try:
                streamData = str(streamData)
                streamData = streamData.split(':')
                if ('null' in streamData[6]):
                    isStreaming = 'false'
                else:
                    isStreaming = 'true'

                errFlag = 1

            except:
                errFlag = 2
                isStreaming = 'null'

        return(isStreaming,errFlag)



    def getFollowerCount(self,userName):
        errFlag = 0

        try:
            try:
                url = 'https://api.twitch.tv/kraken/channels/'+userName+'/follows?limit=1'
            except TypeError:
                url = 'https://api.twitch.tv/kraken/channels/'+str(userName)+'/follows?limit=1'

            try:
                followerData = urlopen(url)
                followerData = followerData.read()
                followerData = followerData.decode()
                followers = loads(followerData)['_total']
                followers = int(followers)


            except TypeError:
                #currently broken
                followerData = urlopen(url)
                followerData = followerData.read()
                followerData = str(followerData)
                followers = int(followerData.split(':')[1].split(',')[0])

                errFlag = 2

        except:
            errFlag = 1
            followers = 'null'

        return(followers,errFlag)


    def getNewFollowers(self,userName,lastCheck,newCheck):
        errFlag = 0
        delta = -1

        try:
            delta = newCheck - lastCheck

        except TypeError:
            try:
                delta = int(newCheck) - int(lastCheck)

            except ValueError:
                errFlag = 1
                followers = ['null']

        except:
            followers = ['null']
            errFlag = errFlag + 1

        if(delta == 0):
            followers = ['null']
            errFlag = errFlag + 10

        elif(delta >= 1):
            if(delta <= 100):
                (followers,errorflag) = getNewFollowersNames(userName,delta,0)
                followers = followers

            else:
                (followers,errorflag) = getNewFollowersNames(userName,100,0)
                followers = followers
        else:
            followers = ['null']
            errFlag = errFlag + 3

        return(followers,errFlag,delta)

    def getNewFollowersNames(self,userName,limit,offset):
        errFlag = 0
        followers = []

        try:
            int(limit)
            int(offset)
        except:
            followers = ['null']
            errFlag = -1
            return(followers,errFlag)

        if(limit == 0):
            followers = ['null']
            return(followers,errFlag)

        try:
            if(limit > 100 or offset < 0):
                errFlag = 1
                followers = ['null']

                return(followers,errFlag)
            else:

                url = 'https://api.twitch.tv/kraken/channels/'
                url = url + str(userName) + '/follows?direction=DESC&limit='
                url = url + str(limit)
                url = url + '&offset='
                url = url + str(offset)

                try:
                    followerData = urlopen(url)
                    followerData = followerData.read()

                    followerData = followerData.decode()
                    followerData = loads(followerData)

                    for i in range(0, limit):
                        followers.append(followerData['follows'][i]['user']['display_name'])

                except:
                    #currently broken
                    followerData = urlopen(url)
                    followerData = followerData.read()

                    followerData = str(followerData)

                    for i in range(0, limit):
                        followers.append(followerData.split(':')[15 + i*22])
                        followers[i] = followers[i].split(',')[0].strip('"')

                    errFlag = 3

        except:
            errFlag = 2
            followers = ['null']

        return(followers,errFlag)



    def getLiveViewerCount(self,streamData):
        errFlag = 0

        try:
            currentlyViewing = loads(streamData.decode())
            currentlyViewing = currentlyViewing['stream']['viewers']
        except:
            try:
                streamData = str(streamData)
                currentlyViewing = int(streamData.split(':')[9].split(',')[0])
                errFlag = 1

            except:
                errFlag = 2
                currentlyViewing = 'null'

        return(currentlyViewing,errFlag)


    def getGameTitle(self,streamData):
        errFlag = 0
        try:
            streamData = loads(streamData.decode())
            gameTitle = streamData['stream']['game']
        except:
            try:
                streamData = str(streamData)
                gameTitle = streamData.split(':')[8].split(',')[0].strip('"')
                errFlag = 1

            except:
                errFlag = 2
                gameTitle = 'null'

        return(gameTitle,errFlag)

    def getAuthorization(self,userName):
        errFlag = 0

        try:
            #need to get from data module
            1/0

        except:
            errFlag = 1
            passToken = 0

        return(passToken,errFlag)

    def getStreamStatus(self,streamData):
        errFlag = 0

        try:
            streamData = loads(streamData.decode())
            streamStatus = streamData['stream']['channel']['status']
        except:
            errFlag = 1
            streamStatus = 'null'

        return(streamStatus,errFlag)

    def getLatestSubscribers(userName,quantity):
        pass

    def getLatestFollowers(self,userName,quantity):
        (followers,errorflag) = self.getNewFollowers(userName,0,quantity)
        return(followers)

    def getLatestFollower(self,userName):
        (followers,errorflag) = self.getNewFollowers(userName,0,1)
        return(followers)

    def getAllFollowers(self,userName):
        followers = []
        (count,error1) = self.getFollowerCount(userName)
        if(error1==0):
            i=0
            ii=0
            error2list = []
            while(i<count):
                ii = ii + 1
                if(i+100<=count):
                    (following,error2)=self.getNewFollowersNames(userName,100,i)
                    if(error2==0):
                        followers.extend(following)
                    else:
                        error2list.extend(['Count ',i,' and error ',error2])
                    i = i + 100
                else:
                    (following,error2)=self.getNewFollowersNames(userName,count-i,i)
                    if(error2==0):
                        followers.extend(following)
                    else:
                        error2list.extend(['Count- ',i,' and error ',error2])
                    break

                if(ii>10000):#temporary glass ceiling - need a timer
                    error2list.append('Too many iterations.')
                    break

            errFlag = error2list
            if(count != len(followers)):
                errFlag = 'Not all followers found after '+str(ii)+' requests.'

        else:
            errFlag = 1

        followers.reverse()
        #TODO: write to file
        return(followers,errFlag)

    def getAllSubscribers(self,userName):
        pass

    def getAlSubscribing(self,userName):
        pass

    def getAllFollowing(self,userName):
        followings = []
        (count,error1) = self.getFollowingCount(userName)
        if(error1==0):
            i=0
            ii=0
            error2list = []
            while(i<count):
                ii = ii + 1
                if(i+100<=count):
                    (following,error2)=self.getFollowingNames(userName,100,i)
                    if(error2==0):
                        followings.extend(following)
                    else:
                        error2list.extend(['Count ',i,' and error ',error2])
                    i = i + 100
                else:
                    (following,error2)=self.getFollowingNames(userName,count-i,i)
                    if(error2==0):
                        followings.extend(following)
                    else:
                        error2list.extend(['Count- ',i,' and error ',error2])
                    break

                if(ii>10000):#temporary glass ceiling - need a timer
                    error2list.append('Too many iterations.')
                    break

            errFlag = error2list
            if(count != len(followings)):
                errFlag = 'Not all followers found after '+str(ii)+' requests.'

        else:
            errFlag = 1

        followings.reverse()
        #TODO: write to file
        return(followings,errFlag)

    def getFollowingCount(self,userName):
        errFlag = 0

        try:
            try:
                url = 'https://api.twitch.tv/kraken/users/'+userName+'/follows/channels?limit=1'
            except TypeError:
                url = 'https://api.twitch.tv/kraken/users/'+str(userName)+'/follows/channels?limit=1'

            try:
                followingData = urlopen(url)
                followingData = followingData.read()
                followingData = followingData.decode()
                followings = loads(followingData)['_total']
                followings = int(followings)


            except TypeError:
                #currently broken
                followingData = urlopen(url)
                followingData = followingData.read()
                followingData = str(followingData)
                followings = int(followingData.split(':')[1].split(',')[0])

                errFlag = 2

        except:
            errFlag = 1
            followings = 'null'

        return(followings,errFlag)


    def getFollowingNames(self,userName,limit,offset):
        errFlag = 0
        followings = []

        try:
            int(limit)
            int(offset)
        except:
            followers = ['null']
            errFlag = -1
            return(followings,errFlag)

        if(limit == 0):
            followings = ['null']
            return(followings,errFlag)

        try:
            if(limit > 100 or offset < 0):
                errFlag = 1
                followings = ['null']

                return(followings,errFlag)
            else:
                url = 'https://api.twitch.tv/kraken/users/'
                url = url + str(userName) + '/follows/channels?direction=DESC&limit='
                url = url + str(limit)
                url = url + '&offset='
                url = url + str(offset)

                try:
                    followingData = urlopen(url)
                    followingData = followingData.read()

                    followingData = followingData.decode()
                    followingData = loads(followingData)

                    #switch to xrange?
                    for i in range(0, limit):
                        followings.append(followingData['follows'][i]['channel']['display_name'])

                except:
                    #currently broken
                    followingData = urlopen(url)
                    followingData = followingData.read()
                    followingData = str(followingData)

                    for i in range(0, limit):
                        followings.append(followingData.split(':')[15 + i*22])
                        followings[i] = followings[i].split(',')[0].strip('"')

                    errFlag = 3

        except:
            errFlag = 2
            followers = ['null']

        return(followings,errFlag)

    def updateAllFollowers(self,userName,filePath):
        pass

    def updateAllFollowing(self,userName,filePath):
        pass

    def updateAllSubscribers(self,userName,filePath):
        pass

    def updateAllSubscribing(self,userName,filePath):
        pass

    def findLiveStreamerFromFollowing(self,userName):
        #give preferrence to same gametitle
        pass
