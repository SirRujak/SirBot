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

#import assets and pass to data object
import lib.sirbot.loader as loader

config = loader.load()

#import main runtime classes
import lib.sirbot.infrastructure as infrastructure
import lib.sirbot.application as application

if(config.GUI == True):
    import lib.sirbot.interface as interface



#import shutdown module
import lib.sirbot.shutdown as shutdown

if __name__ == '__main__':

    #initialize primary modules
    infra = infrastructure.infrastructure(config)
    app = application.application(config)
    if(config.GUI == True):
        inter = interface.interface(config)
    
    #runtime loop - single thread
    if(config.GUI == True):
        while(ON):
            ON = ON * infra.tick()
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


