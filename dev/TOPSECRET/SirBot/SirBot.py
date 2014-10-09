# -*- coding: utf-8 -*-

#main sirbot script
ON = 1

try:
    import lib.sirbot.initialize as initialize

    #display splash
    initialize.splash()

    #run validation
    initialize.validate()

except:
    try:
        import lib.sirbot.setup as setup
        #open a terminal or something to let them know we are working
        #run setup
        import lib.sirbot.initialize as initialize

        #display splash
        initialize.splash()

        #run validation
        initialize.validate()
        
    except:
        #display/log error
        #end script
        pass

#import configurations 
import lib.sirbot.configloader as configloader

config = configloader.load()

#import main runtime classes
import lib.sirbot.network as network
import lib.sirbot.application as application

if(config.GUI == True):
    import lib.sirbot.interface as interface
    import lib.sirbot.assetloader as assetloader

#import shutdown module
import lib.sirbot.shutdown as shutdown

#import tools
from multiprocessing import Queue

if __name__ == '__main__':

    #initialize primary modules and queues
    netinput = Queue()
    netoutput = Queue()
    net = network.network(config,netinput,netoutput)
    if(config.GUI == True):
        interinput = Queue()
        interoutput = Queue()
        inter = interface.interface(config,interinput,interoutput)
        app = application.application(config,
                                      netinput,netoutput,
                                      interinput,interoutput)
    else:
        app = application.application(config,netinput,netoutput)
    
    #runtime loop - single thread
    if(config.GUI == True):
        while(ON):
            ON = ON * net.tick()
            ON = ON * app.tick()
            ON = ON * inter.tick()

        infra.shutdown()
        app.shutdown()
        inter.shutdown()
        
    else:
        while(ON):
            ON = ON * infra.tick()
            ON = ON * app.tick()

        infra.shutdown()
        app.shutdown()

    #send current configuration options to be saved for next startup
    shutdown.shutdown(config)


