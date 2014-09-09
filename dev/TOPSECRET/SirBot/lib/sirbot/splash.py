# -*- coding: utf-8 -*-

#simple script for importing splash assets and displaying splash screen

from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Tk
from tkinter import Label

def splash():
    try:
        splashimage = PhotoImage(file='splash.gif')
        loadingSplash = Tk()
        loading = ttk.Label(loadingSplash,image=self.splashimage)
        loadingSplash.overrideredirect(True)
        loading.pack()

        h = loading.winfo_screenheight()
        w = loading.winfo_screenwidth()

        loadingSplash.wm_attributes('-alpha',0.75)
        loadingSplash.update_idletasks()
        loadingSplash.geometry('262x112+'+str(int(w/2)-131*1)+
                                    '+'+str(int(h/2)-56*1))
        loadingSplash.update_idletasks()
        loadingSplash.update()
    except:
        #log
        loadingSplash = Tk()
        #myfont = tkFont.families()[0]
        loading = Label(loadingSplash,text='SirBot')
        loadingSplash.overrideredirect(True)
        loading.pack()

        h = loading.winfo_screenheight()
        w = loading.winfo_screenwidth()

        loadingSplash.wm_attributes('-alpha',0.75)
        loadingSplash.update_idletasks()
        loadingSplash.geometry('262x112+'+str(int(w/2)-131*1)+
                               '+'+str(int(h/2)-56*1))
        loadingSplash.update_idletasks()
        loadingSplash.update()

def destroy():
    try:
        loadingSplash.destroy()
    except:
        #log
        pass
    
