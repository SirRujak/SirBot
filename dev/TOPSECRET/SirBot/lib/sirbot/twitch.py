# -*- coding: utf-8 -*-

#class for interfacing with twitch.tv

from urllib.request import urlopen
from json import loads

class twitch():
    def getStreamInfo(userName):
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


    def getTwitchState(streamData):
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



    def getFollowerCount(userName):
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


    def getNewFollowers(userName,lastCheck,newCheck):
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

    def getNewFollowersNames(userName,limit,offset):
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



    def getLiveViewerCount(streamData):
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


    def getGameTitle(streamData):
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

    def getAuthorization(userName):
        errFlag = 0

        try:
            #need to get from data module
            1/0

        except:
            errFlag = 1
            passToken = 0

        return(passToken,errFlag)

    def getStreamStatus(streamData):
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

    def getLatestFollowers(userName,quantity):
        (followers,errorflag) = self.getNewFollowers(userName,0,quantity)
        return(followers)

    def getAllFollowers(userName):
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

    def getAllSubscribers(userName):
        pass

    def getALlSubscribing(userName):
        pass

    def getAllFollowing(userName):
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

    def getFollowingCount(userName):
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


    def getFollowingNames(userName,limit,offset):
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

    def updateAllFollowers(userName,filePath):
        pass

    def updateAllFollowing(userName,filePath):
        pass

    def updateAllSubscribers(userName,filePath):
        pass

    def updateAllSubscribing(userName,filePath):
        pass

    def findLiveStreamerFromFollowing(userName):
        #give preferrence to same gametitle
        pass
