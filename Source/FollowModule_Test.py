import urllib.request

response = urllib.request.urlopen('https://api.twitch.tv/kraken/streams/eneija')
html = response.read().decode()
#html = str( html, encoding='utf8' )
print(html[1])
html = html.split(",")
print(html)
