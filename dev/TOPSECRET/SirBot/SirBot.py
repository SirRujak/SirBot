# -*- coding: utf-8 -*-

#main sirbot script
ON = True

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

import lib.sirbot.assetloader as assetloader

#import assets and pass to data object

import lib.sirbot.dataloader as dataloader

#import configurations and pass to data object


#import main runtime class
import lib.sirbot.main as main

#perform internal imports for main.py
main.imports()

#import shutdown module
import lib.sirbot.shutdown as shutdown

#runtime loop
while(ON):
    ON = main.main.run()

shutdown.shutdown()


