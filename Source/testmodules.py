import twitchData as twitchdatafetch
import json

modules = ['twitchData']
response='null'
username='twitchplayspokemon'
num=1

def testtwitchData():
    username = input('Which channel would you like to scope? ')
    num = input('How many recent followers would you like to fetch? ')
    num=int(num)
    if(num>100):
        num = 100
    (streamdata,errorflag)=twitchdatafetch.getStreamInfo(username)
    if(errorflag!=0 and errorflag!='0'):
        print('Error code in data fetch: ',end='')
        print(errorflag)
    print('\n')
    print('---INFO---\n')
    print(username)
    streamstate =twitchdatafetch.getTwitchState(streamdata)[0]
    print('streaming: ' + streamstate)
    if(streamstate == 'true'):
        print('playing: ' + str(twitchdatafetch.getGameTitle(streamdata)[0]))
        print('status: ' + str(twitchdatafetch.getStreamStatus(streamdata)[0]))
        print('# currently viewing: ' + str(twitchdatafetch.getLiveViewerCount(streamdata)[0]))
    print('followers: ' + str(twitchdatafetch.getTwitchFollowCount(username)[0]))
    print(str(num)+' most recent: ' + str(twitchdatafetch.getNewFollows(username,0,num)[0]))
    getlist = input('Fetch follower list? ')
    if(getlist=='Yes'):
        f=twitchdatafetch.getTwitchFollowCount(username)[0]
        v=twitchdatafetch.getAllFollows(username)
        print('A list of all ',end='')
        print(f,end='')
        print(' of ',end='')
        print(username,end='')
        print("'s followers:")
        print(v[0])
        if(v[1]):
            print("Error: ",end='')
            print(v[1])

    print('\n')

def testdummy():
    print('Nothing here!')

while(response!='quit'):
    response = input('Which module would you like to test? ')

    if(response=='twitchData'):

        testtwitchData()

    elif(response=='dummy'):
        testdummy()

    elif(response.lower()=='stop'or response=='terminate'or response=='exit'):
        response = 'quit'

    elif(response.lower()=='close'or response=='break'or response=='end'):
        response = 'quit'

    elif(response.lower()=='none'):
        response='quit'
