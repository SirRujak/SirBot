import twitchData as twitch
import json

modules = ['twitchData']
response='null'
username='twitchplayspokemon'
num=1

def test_twitchData():
    username = input('Which channel would you like to scope? ')
    num = input('How many recent followers would you like to fetch? ')
    num=int(num)
    if(num>100):
        num = 100
    (streamdata,errorflag)=twitch.getStreamInfo(username)
    if(errorflag!=0 and errorflag!='0'):
        print('Error code in data fetch: ',end='')
        print(errorflag)
    print('\n')
    print('---INFO---\n')
    print(username)
    streamstate =twitch.getTwitchState(streamdata)[0]
    print('streaming: ' + streamstate)
    if(streamstate == 'true'):
        print('playing: ' + str(twitch.getGameTitle(streamdata)[0]))
        print('status: ' + str(twitch.getStreamStatus(streamdata)[0]))
        print('# currently viewing: ' + str(twitch.getLiveViewerCount(streamdata)[0]))
    print('followers: ' + str(twitch.getFollowerCount(username)[0]))
    print(str(num)+' most recent: ' + str(twitch.getNewFollowers(username,0,num)[0]))
    getlist = input('Fetch follower list? (Note:-Large processor and network load incurred) ')
    if(getlist=='yes'):
        f=twitch.getFollowerCount(username)[0]
        v=twitch.getAllFollowers(username)
        print('A list of all ',end='')
        print(f,end='')
        print(' of ',end='')
        print(username,end='')
        print("'s followers:")
        print(v[0])
        if(v[1]):
            print("Error: ",end='')
            print(v[1])
    print('channels followed: '+str(twitch.getFollowingCount(username)[0]))
    getlist = input('Fetch following list? (Note:-Large processor and network load incurred) ')
    if(getlist=='yes'):
        f=twitch.getFollowingCount(username)[0]
        v=twitch.getAllFollowing(username)
        print('A list of all ',end='')
        print(f,end='')
        print(' channels ',end='')
        print(username,end='')
        print(" is following:")
        print(v[0])
        if(v[1]):
            print("Error: ",end='')
            print(v[1])

    print('\n')

def testdummy():
    print('Nothing here!',end='')
    time.sleep(5)
    print('..yet...')

while(response!='quit'):
    response = input('Which module would you like to test? ')
    
    if(response=='list'or response=='ls'):
        print(modules)
        
    if(response=='twitchData'):
        test_twitchData()

    if(response=='dummy'):
        testdummy()

    response=response.lower()
    
    if(response=='stop'or response=='terminate'or response=='exit'):
        response = 'quit'

    if(response=='close'or response=='break'or response=='end'):
        response = 'quit'

    if(response=='none'or response=='cancel'):
        response='quit'
