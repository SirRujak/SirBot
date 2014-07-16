import urllib.request
import json
##import time

def getStreamInfo(userName):
    errFlag = 0
    try:
        try:
            url = 'https://api.twitch.tv/kraken/streams/' + userName
        except TypeError:
            url = 'https://api.twitch.tv/kraken/streams/' + str(userName)
        streamData = urllib.request.urlopen(url)
        streamData = streamData.read()

    except:
        errFlag = 1
        streamData = 0

    return(streamData,errFlag)


def getTwitchState(streamData):
    errFlag = 0
    try:
        streamData = json.loads(streamData.decode())
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



def getTwitchFollowCount(userName):
    errFlag = 0

    try:
        try:
            url = 'https://api.twitch.tv/kraken/channels/'+userName+'/follows?limit=1'
        except TypeError:
            url = 'https://api.twitch.tv/kraken/channels/'+str(userName)+'/follows?limit=1'

        try:
            followData = urllib.request.urlopen(url)
            followData = followData.read()
            followData = followData.decode()
            follows = json.loads(followData)['_total']
            follows = int(follows)


        except TypeError:
            #currently broken
            followData = urllib.request.urlopen(url)
            followData = followData.read()
            followData = str(followData)
            follows = int(followData.split(':')[1].split(',')[0])

            errFlag = 2

    except:
        errFlag = 1
        follows = 'null'

    return(follows,errFlag)


def getNewFollows(userName,lastCheck,newCheck):
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
            (followers,errorflag) = getNewFollowsNames(userName,delta,0)
            followers = followers

        else:
            (followers,errorflag) = getNewFollowsNames(userName,100,0)
            followers = followers
    else:
        followers = ['null']
        errFlag = errFlag + 3

    return(followers,errFlag,delta)

def getNewFollowsNames(userName,limit,offset):
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
                followData = urllib.request.urlopen(url)
                followData = followData.read()

                followData = followData.decode()
                followData = json.loads(followData)

                for i in range(0, limit):
                    followers.append(followData['follows'][i]['user']['display_name'])

            except:
                #currently broken
                followData = urllib.request.urlopen(url)
                followData = followData.read()

                followData = str(followData)

                for i in range(0, limit):
                    followers.append(followData.split(':')[15 + i*22])
                    followers[i] = followers[i].split(',')[0].strip('"')

                errFlag = 3

    except:
        errFlag = 2
        followers = ['null']

    return(followers,errFlag)



def getLiveViewerCount(streamData):
    errFlag = 0

    try:
        currentlyViewing = json.loads(streamData.decode())
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
        streamData = json.loads(streamData.decode())
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
        passToken = str(open("config","rb+").read().decode().split("\n")[2].split('%')[1])
        passToken = 'oauth:' + passToken

    except:
        errFlag = 1
        passToken = 0

    return(passToken,errFlag)

def getStreamStatus(streamData):
    errFlag = 0

    try:
        streamData = json.loads(streamData.decode())
        streamStatus = streamData['stream']['channel']['status']
    except:
        errFlag = 1
        streamStatus = 'null'

    return(streamStatus,errFlag)

def getLatestSubscribers(userName,quantity):
    pass

def getLatestFollowers(userName,quantity):
    (follows,errorflag) = getNewFollows(userName,0,quantity)
    return(follows)

def getAllFollows(userName):
    followers = []
    (count,error1) = getTwitchFollowCount(userName)
    if(error1==0):
        i=0
        ii=0
        error2list = []
        while(i<count):
            ii = ii + 1
            if(i+100<=count):
                (following,error2)=getNewFollowsNames(userName,100,i)
                if(error2==0):
                    followers.extend(following)
                else:
                    error2list.extend(['Count ',i,' and error ',error2])
                i = i + 100
            else:
                (following,error2)=getNewFollowsNames(userName,count-i,i)
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
    return(followers,errFlag)

def getAllSubscribers(userName):
    pass




