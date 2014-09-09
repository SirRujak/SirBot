try:
    import lib.initialize as initialize

    #display splash
    initialize.splash()

    #run validation
    initialize.validate()

except:
    try:
        import lib.setup as setup
        #open a terminal or something to let them know we are working
        #run setup
        import lib.initialize as initialize

        #display splash
        initialize.splash()

        #run validation
        initialize.validate()
        
    except:
        #display/log error
        #end script
        pass

import lib.assetloader as assetloader

#import assets and pass to data object

import lib.dataloader as dataloader

#import configurations and pass to data object

