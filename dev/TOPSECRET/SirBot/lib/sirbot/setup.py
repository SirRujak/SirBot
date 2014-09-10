# -*- coding: utf-8 -*-

#script to run before first use that creates all necessary config files
#and file structures. uses fetcher to download assets/libs if necessary

import fetcher
from json import dump

def createConfigFile():
        configDict = {}
        configDict["CHANNEL-INFO"] = {"USERNAME":None, "CHANNEL":None, "PASSWORD":None}
        configDict["SOCKET-INFO"] = {"MAX-SOCKETS":None}
        configDict["SPAM-INFO"] = {"SPAM-LEVEL":None, "SPAM-FILE-NAME":None}
        configDict["PREFRENCES"] = {}
        moduleDir=dirname(__file__)
        moduleDir=moduleDir.rsplit('/',3)[0]
        configPath=molduleDir+'/config/sirbot/config'
        configFile = open(configPath, 'w')
        dump(configDict, configFile)
        configFile.close()

def setConfigDefaults():
    #set default values for some config options
    pass

def createFileStructure():
    #create file structure using os
    pass


