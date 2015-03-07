# -*- coding: utf-8 -*-

#main sirbot script
ON = 1
SPLASH = 1

##try:
import lib.sirbot.initialize as initialize

if(SPLASH == 1):
    #display splash
    splash = initialize.splashing()
    root = splash.root()

#import configurations 
from lib.sirbot.configloader import configloader

config = configloader()

#import main runtime classes
from lib.sirbot.application import application
if(config['GUI'] == 1):
    from lib.sirbot.interfaceDEV import interface
    from lib.sirbot.assetloader import assetloader

#import shutdown module
from lib.sirbot.shutdown import shutdown

#import tools
from multiprocessing import Queue
from time import sleep



if __name__ == '__main__':

    #initialize primary modules and queues
##    if(config['GUI'] == 1):
##        interinput = Queue()
##        interoutput = Queue()
    assets = assetloader()
    app = application(config,assets,root)#,interinput,interoutput)
##        inter = interface(config,assets,interinput,interoutput,root)
##    else:
##        app = application(config)

    #destroy splash
    if(SPLASH == True):
##        sleep(1)
        splash.destroySplash()
    
    #runtime loop - single thread
##    idle = 0.01
##    if(config['GUI'] == 1):
    app.startup()
##        inter.display()
##        app.begin()#temporary
    while(ON):
        ON = ON * app.tick()
##            ON = ON * inter.tick()
##            sleep(idle)

    app.shutdown()
##        inter.shutdown()
        
##    else:
##        app.begin()#temporary
##        while(ON):
##            ON = ON * app.tick()
####            sleep(idle)
##
##        app.shutdown()

    #send current configuration options to be saved for next startup
##    if(config['GUI'] == 1):
##        shutdown(config,interinput,interoutput)
##    else:
    shutdown(config)

##except:
##    pass
