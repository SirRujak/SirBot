#script to rule all startup/import scripts

def splash():
    try:
        import lib.splash as splash
        #display splash

    except:
        #open a terminal or something to let them know we are gathering assets
        pass

def validate():
    try:
        import lib.validator as validator
        #run validator

    except:
        try:
            import lib.setup as setup
            #open a terminal or something to let them know we are working
            #run setup

        except:
            #display/log error
            #end script
            pass
    
