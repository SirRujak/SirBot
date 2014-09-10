# -*- coding: utf-8 -*-

#script for loading all audio and visual sirbot assets - except for splash assets

from tkinter import PhotoImage

def assetloader():
    moduleDir=dirname(__file__)
    moduleDir=moduleDir.rsplit('/',2)[0]
    assetPath=moduleDir+'/resource/sirbot/'
    
    configFile = open(configPath,"rb+")
    data = configFile.read().decode()
    data = loads(data)
    configFile.close()

    try:
        filename = assetPath+'Sirbot.gif'
        self.logoimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'userslist.gif'
        self.userslistimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'options.gif'
        self.optionsimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'dashboard.gif'
        self.dashboardimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'chat.gif'
        self.chatimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'users.gif'
        self.usersimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'commands.gif'
        self.commandsimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'advanced.gif'
        self.advancedimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass
    try:
        filename = assetPath+'help.gif'
        self.helpimage = tk.PhotoImage(file=filename)
    except:
        #log
        pass


    return(data)
