# -*- coding: utf-8 -*-

#simple script for loading configurations into memory

from json import loads
from os.path import dirname



def configloader():
    moduleDir=dirname(__file__)
    moduleDir=moduleDir.rsplit('\\',2)[0]
    configPath=moduleDir+'\\config\\sirbot\\config'

    try:
        configFile = open(configPath,"rb+")
        data = configFile.read().decode()
        data = loads(data)
        configFile.close()
    except:
        #generate config object
        config={}
        #set GUI default to ON
        config['GUI']=1
        #set interface defaults
        config['Interface']={}
        config['Interface']['motd']='Hello world!'
        config['Interface']['map']='620x540+50+50'
        config['Interface']['remember position']=0
        config['Interface']['iconified']=0
        config['Interface']['user list']={}
        config['Interface']['user list']['start open']=0
        config['Interface']['user list']['show channels']=1
        config['Interface']['user list']['show groups']=1
        config['Interface']['user list']['sort']='alphanumeric'
        config['Interface']['options menu']={}
        config['Interface']['options menu']['start open']=0
        config['Interface']['options menu']['default tab']='dashboard'
        config['Interface']['send as']='trusted'
        config['Interface']['target channel']=0
        config['Interface']['chat']={}
        config['Interface']['chat']['timestamps']=0
        config['Interface']['chat']['user colors']=1
        config['Interface']['chat']['emoticons']=1
        config['Interface']['chat']['actions']=1
        config['Interface']['chat']['raw']=0
        config['Interface']['chat']['channel tag']=0
        config['Interface']['chat']['text color']='#000000'
        config['Interface']['chat']['silent']=0
        #set accounts defaults
        config['Twitch Accounts']={}
        config['Twitch Accounts']['automated account']={}
        config['Twitch Accounts']['automated account']['name']=0
        config['Twitch Accounts']['automated account']['token']=0
        config['Twitch Accounts']['trusted account']={}
        config['Twitch Accounts']['trusted account']['name']=0
        config['Twitch Accounts']['trusted account']['token']=0
        config['Twitch Accounts']['trusted account']['join chat']=1
        #set channel defaults
        config['Twitch Channels']={}
        config['Twitch Channels']['default channel']=0
        config['Twitch Channels']['favorite channels']=[]
        #set automation defaults
        config['Twitch Automated Moderator']={}
        config['Twitch Automated Moderator']['welcome users']=0
        config['Twitch Automated Moderator']['echo']=0
        config['Twitch Automated Moderator']['monitor chat content']=0
        config['Twitch Automated Moderator']['allow commands']=1
        config['Twitch Automated Moderator']['watch for followers']=0
        config['Twitch Automated Moderator']['watch for subscribers']=0
        #set miscelleneous defaults
        config['MISC']={}
        config['MISC']['twitch connect retries']=1
        config['MISC']['twitchclient']=0
        #set dummmy path
        config['Path']=0

        data = config
        
    data['path'] = moduleDir
    return(data)
