# -*- coding: utf-8 -*-

#simple script for loading configurations into memory

from json import loads
from os.path import dirname



def dataloader():
    moduleDir=dirname(__file__)
    moduleDir=moduleDir.rsplit('/',3)[0]
    configPath=moduleDir+'/config/sirbot/config'
    
    configFile = open(configPath,"rb+")
    data = configFile.read().decode()
    data = loads(data)
    configFile.close()

    return(data)
