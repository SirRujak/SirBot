# -*- coding: utf-8 -*-

#class that contains calls to mainloop/updatetasks of subordinate classes
#implement prioritization and optimization structures
#may contain elements to monitor system utilization

#import all subordinate modules
def imports():
    import data
    import interface
    import network
    import ai
    import twitch
    import irc
    import logger
    import player
    import streamer
    import obs
    import voice
    import help

#main class
class main():
    #this is where all submodules need to speak to each other and we run loops
    
