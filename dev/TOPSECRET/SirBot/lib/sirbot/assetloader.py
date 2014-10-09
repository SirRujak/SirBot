# -*- coding: utf-8 -*-

#script for loading all audio and visual sirbot assets - except for splash assets

from tkinter import PhotoImage
from os.path import dirname

def assetloader():
    moduleDir=dirname(__file__)
    moduleDir=moduleDir.rsplit('/',3)[0]
    assetPath=moduleDir+'/resources/sirbot/'

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
