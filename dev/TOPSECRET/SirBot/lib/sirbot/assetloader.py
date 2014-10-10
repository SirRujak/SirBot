# -*- coding: utf-8 -*-

#script for loading all audio and visual sirbot assets - except for splash assets

from os.path import dirname

class assetloader():
    def __init__(self):
        self.moduleDir=dirname(__file__)
        self.moduleDir=self.moduleDir.rsplit('\\',2)[0]
        self.assetPath=self.moduleDir+'\\resources\\sirbot\\'

#        try:
        filename = self.assetPath+'Sirbot.gif'
        self.logoimage = (filename)
#        except:
            #log
#            pass
        try:
            filename = self.assetPath+'userslist.gif'
            self.userslistimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'options.gif'
            self.optionsimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'dashboard.gif'
            self.dashboardimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'chat.gif'
            self.chatimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'users.gif'
            self.usersimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'commands.gif'
            self.commandsimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'advanced.gif'
            self.advancedimage = (filename)
        except:
            #log
            pass
        try:
            filename = self.assetPath+'help.gif'
            self.helpimage = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'down.gif'
            self.dwn = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'down2.gif'
            self.dwn2 = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'up.gif'
            self.up = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'up2.gif'
            self.up2 = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'enter.gif'
            self.enterimage = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'enter2.gif'
            self.enterimage2 = filename
        except:
            #log
            pass
        try:
            filename = self.assetPath+'optheader.gif'
            self.optheader = filename
        except:
            #log
            pass


