# -*- coding: utf-8 -*-

#simple script for importing splash assets and displaying splash screen

from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Tk,Toplevel
#from tkinter import Label
from os.path import dirname

class splash():
#    try:
    def __init__(self):
        moduleDir = dirname(__file__)
        moduleDir = moduleDir.replace('\\','/').rsplit('/')[0]
        image = moduleDir+'/resources/sirbot/splash.gif'
        self.root = Tk()
        self.root.withdraw()
        self.loadingSplash = Toplevel()
        splashimage = PhotoImage(file=image)
        self.loading = ttk.Label(self.loadingSplash,image=splashimage)
        self.loadingSplash.overrideredirect(True)
        self.loading.pack()

        h = self.loading.winfo_screenheight()
        w = self.loading.winfo_screenwidth()

        self.loadingSplash.wm_attributes('-alpha',0.75)
        self.loadingSplash.update_idletasks()
        self.loadingSplash.geometry('262x112+'+str(int(w/2)-131*1)+
                                    '+'+str(int(h/2)-56*1))
        self.loadingSplash.update_idletasks()
        self.loadingSplash.update()
        
#    except:
##        #log
##        loadingSplash = Tk()
##        #myfont = tkFont.families()[0]
##        loading = Label(loadingSplash,text='SirBot')
##        loadingSplash.overrideredirect(True)
##        loading.pack()
##
##        h = loading.winfo_screenheight()
##        w = loading.winfo_screenwidth()
##
##        loadingSplash.wm_attributes('-alpha',0.75)
##        loadingSplash.update_idletasks()
##        loadingSplash.geometry('262x112+'+str(int(w/2)-131*1)+
##                               '+'+str(int(h/2)-56*1))
##        loadingSplash.update_idletasks()
##        loadingSplash.update()

    def destroy(self):
        try:
            self.loadingSplash.destroy()
        except:
            #log
            pass

    def getroot(self):
        return(self.root)
    
