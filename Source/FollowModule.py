import requests
import time
##check if she is streaming at https://api.twitch.tv/kraken/streams/eneija
##third follower is ?limit=3&offset=2
##r = requests.get('https://api.twitch.tv/kraken/channels/eneija/follows?limit=1')
##s = r.json()
##t = s['follows']
##for item in range(len(t)):
##    print(t[item]['user']['display_name'])
##    print(t[item]['created_at'])
##print(s['_total'])

def startUp():
    fullListing = requests.get('https://api.twitch.tv/kraken/channels/eneija/follows')
    jsonListing = fullListing.json()
    initialTotal = jsonListing['_total']
    return initialTotal
##    print(initialTotal)

def getTotalAndList():
    fullListing = requests.get('https://api.twitch.tv/kraken/channels/eneija/follows')
    jsonListing = fullListing.json()
    totalFollowers = jsonListing['_total']
    namesListing = jsonListing['follows']
    namesList = []
    for item in range(len( namesListing )):
        namesList.append(namesListing[item]['user']['display_name'])
    namesList.append(totalFollowers)
    return(namesList)
    


def mainFunc():
    currentTotal = startUp()
    x = 0
    while x < 1:
        time.sleep(60)
        totalAndList = getTotalAndList()
        if (totalAndList[25] - currentTotal > 0):
            pass
        currentTotal = totalAndList[25]
        print(currentTotal)
        x+=1
    print("done")

mainFunc()
            
