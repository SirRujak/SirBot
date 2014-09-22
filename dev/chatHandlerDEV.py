###############################################################
###############################################################

## NEW COMMAND PARSING AREA
class chatHandler:
        ## Needs variables for chatData, command dictionary
        ## Needs functions for loading & unloading command dictionary
        ## Needs fucntions for checking the kind of command it is
        ## Needs functions for splitting up multi commands
        ## Needs functions for adding and removing things from queues
        ## Needs variables for in and out queues
        ## Needs to implement parser and chat level checker
        ## Needs to be able to run at arbitrary chat level
        ## Needs to be able to make a timer
        ## Needs to have all of the base functions made
        ## Base functions are timeout, ban, promote to level, demote to level,
        ## Needs channelName, temp, modList, spamLevel, spamFilter variables where temp is the message
        def __init__():
                pass

        ## Base functions that must be in the API.
        def createTimer(timerData):
                pass
        
        def banUser(userData):
                pass

        def demoteUserToLevel(userData):
                pass

        def promoteUserToLevel(userData):
                pass

        def timeoutUser(userData, timeData):
                pass

        ## Funcitons that should possibly be in the API.
        def joinChannel(channelData):
                pass

        def leaveChannel(channelData):
                pass

        ## Other functions.
        def checkChatCMD(chatData):
                pass

        def splitMultiCMD(multiCMD):
                pass


## Secondary classes.
class chatDataMessage:
        def __init__(self, userName, channelName, timeStamp, messageContents,
                     isLocal, ):
                pass

class channelData:
        def __init__():
                pass


###############################################################
###############################################################
