import urllib.request
##import time

def getStreamInfo(userName):
    errFlag = 0
    
    try:
        url = 'https://api.twitch.tv/kraken/streams/' + userName
        try:
            streamData = urllib.request.urlopen(url)
            streamData = streamData.read()

        except:
            errFlag = 2
            streamData = 0

    except TypeError:
        url = 'https://api.twitch.tv/kraken/streams/' + str(userName)
        try:
            streamData = urllib.request.urlopen(url)
            streamData = streamData.read()
            
        except:
            errFlag = 3
            streamData = 0

    except:
        errFlag = 1
        streamData = 0

    return(streamData,errFlag)


def getTwitchStatus(streamData):
    errFlag = 0
    
    try:
        streamData = str(streamData)
        streamData = streamData.split(':')
        if ('null' in streamData[6]):
            isStreaming = 'false'
        else:
            isStreaming = 'true'

    except:
        errFlag = 1
        isStreaming = 'null'

    return(isStreaming,errFlag)
        


def getTwitchFollowCount(userName):
    errFlag = 0

    try:
        url = 'https://api.twitch.tv/kraken/channels/'+userName+'/follows?limit=1'
        try:
            followData = urllib.request.urlopen(url)
            followData = followData.read()
            followData = str(followData)
            follows = int(followData.split(':')[1].split(',')[0])

        except:
            errFlag = 2
            follows = 'null'

    except TypeError:
        url = 'https://api.twitch.tv/kraken/channels/'+str(userName)+'/follows?limit=1'
        try:
            followData = urllib.request.urlopen(url)
            followData = followData.read()
            follows = int(followData.split(':')[1].split(',')[0])
            
        except:
            errFlag = 3
            follows = 'null'

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

        errFlag = errFlag + 1

    if(delta == 0):
        followers = ['null']

    elif(delta >= 1):
        if(delta <= 100):
            followers = getNewFollowsNames(userName,delta,0)[0:delta-1]
        else:
            followers = getNewFollowsNames(userName,100,0)[0:99]
    else:
        errFlag = 3

    return(followers,errFlag,delta)
            


def getNewFollowsNames(userName,limit,offset):
    errFlag = 0
    followers = []

    if(limit == 0):
        followers = 'null'
        return(followers,errFlag)

    try:
        if(limit > 100 or offset < 0):
            errFlag = 1
            followers = ['null']

            return(followers,errFlag)
        else:
            try:
                url = 'https://api.twitch.tv/kraken/channels/'
                url = url + userName + '/follows?limit='
                url = url + limit
                url = url + '&offset='
                url = url + offset
                try:
                    followData = urllib.request.urlopen(url)
                    followData = followData.read()

                    followData = str(followData)

                    for i in range(0, limit):
                        followers.append(followData.split(':')[15 + i*22])
                        followers[i] = followers[i].split(',')[0].strip('"')

                except:
                    errFlag = 2
                    followers = ['null']
                    

            except TypeError:
                url = 'https://api.twitch.tv/kraken/channels/'
                url = url + str(userName) + '/follows?limit='
                url = url + str(limit)
                url = url + '&offset='
                url = url + str(offset)
                try:
                    followData = urllib.request.urlopen(url)
                    followData = followData.read()

                    followData = str(followData)

                    for i in range(0, limit):
                        followers.append(followData.split(':')[15 + i*22])
                        followers[i] = followers[i].split(',')[0].strip('"')

                except:
                    errFlag = 3
                    followers = ['null']
                
            except:
                errFlag = 4
                followers = ['null']

    except:
        errFlag = 5
        followers = ['null']

    return(followers,errFlag)



def getLiveViewerCount(streamData):
    errFlag = 0

    try:
        streamData = str(streamData)
        currentlyViewing = int(streamData.split(':')[9].split(',')[0])

    except:
        errFlag = 1
        currentlyViewing = 'null'

    return(currentlyViewing,errFlag)


def getGameTitle(streamData):
    errFlag = 0

    try:
        streamData = str(streamData)
        gameTitle = streamData.split(':')[8].split(',')[0].strip('"')

    except:
        errFlag = 1
        gameTitle = 0

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



    

    
