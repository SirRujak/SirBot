# -*- coding: utf-8 -*-

#script containing all pertinent tasks to prepare for software termination.
#successful completion of this process at last runtime, will skip extra validation
#steps on next run

from json import dumps

def shutdown(config,interinput=None,interoutput=None):
    #check for lingering runtime errors
    #finishing writing log queues to file
    #if none: write clean.start file in config directory
    if(config['Interface']['remember position'] == 0):
        config['Interface']['map'] = '620x540+50+50'

    if(config['first run'] == 1):
        config['first run'] = 0
        
    configPath = config['path']+'\\config\\sirbot\\config'    
    configFile = open(configPath,"wb+")
    configData = dumps(config)
    configFile.write(configData)
    configFile.close()

#perhaps add garbage collector control here?
