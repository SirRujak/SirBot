# -*- coding: utf-8 -*-

#script to rule all startup/import scripts

class splashing():
    def __init__(self):
        #try:
        import lib.sirbot.splash
        #display splash
        self.startsplash=splash.splash()

        #except:
            #open a terminal or something to let them know we are gathering assets
            #pass
    def destroySplash(self):
        self.startsplash.destroy()

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
    
