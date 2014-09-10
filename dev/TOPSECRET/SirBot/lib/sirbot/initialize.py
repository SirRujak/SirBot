# -*- coding: utf-8 -*-

#script to rule all startup/import scripts

def splash():
    try:
        import splash
        #display splash
        splash.splash()

    except:
        #open a terminal or something to let them know we are gathering assets
        pass

def validate():
    try:
        import validator
        #run validator

    except:
        try:
            import setup
            #open a terminal or something to let them know we are working
            #run setup

        except:
            #display/log error
            #end script
            pass
    
def destroySplash():
    #destroy splash window
    splash.destroy()
