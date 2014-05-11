import twitchdatafetch

print('---INFO---\n')

username='lliiam'
num=2

streamdata=twitchdatafetch.getStreamInfo(username)

print(username)
print('streaming: ' + twitchdatafetch.getTwitchStatus(streamdata)[0])
print('playing: ' + str(twitchdatafetch.getGameTitle(streamdata)[0]))
print('followers: ' + str(twitchdatafetch.getTwitchFollowCount(username)[0]))
print('2 most recent: ' + str(twitchdatafetch.getNewFollows(username,0,num)[0]))
print('currently viewing: ' + str(twitchdatafetch.getLiveViewerCount(streamdata)[0]))


