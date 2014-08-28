#

try:
    import time
    import tkinter as tk

    from tkinter import ttk

except ImportError:
    try:
        import os
        #collect environmental data for error log
    except:
        #set environmental data to null
        pass

    #write error to logs
    #potentially try to retrieve missing modules
    
    

class GUI():

    def __init__(self):
        self.launch()


    def launch(self):
        self.createMainWindow()

        self.splash()
        self.imports()       
        self.allocateVars()
        self.createChildren()
        #load control values from config

        #run startup tasks eventually
        #including: remember window size/pos from last use; otherwise default
        #meanwhile:
        self.geomMain = '621x541+50+50'
        time.sleep(1)

        self.loadingSplash.destroy()
        self.loadMainWindow()
        self.MainWindow.update_idletasks()

    def imports(self):

        try:
            self.logoimage = tk.PhotoImage(file='sirbot2.gif')
        except:
            #log
            pass
        try:
            self.usersimage = tk.PhotoImage(file='users.gif')
        except:
            #log
            pass
        try:
            self.optionsimage = tk.PhotoImage(file='options.gif')
        except:
            #log
            pass
        

    def splash(self):
        try:
            self.splashimage = tk.PhotoImage(file='Sirbot.gif')
        except:
            #log
            pass
        try:
            self.loadingSplash = tk.Toplevel(self.MainWindow)
            self.loading = ttk.Label(self.loadingSplash,image=self.splashimage)
            self.loadingSplash.overrideredirect(True)
            self.loading.pack()

            top = self.loading.winfo_toplevel()
            self.h = self.loading.winfo_screenheight()
            self.w = self.loading.winfo_screenwidth()
            self.hmm = self.loading.winfo_screenmmheight()
            self.wmm = self.loading.winfo_screenmmwidth()

            self.loadingSplash.wm_attributes('-alpha',0.75)
            self.loadingSplash.update_idletasks()
            self.loadingSplash.geometry('262x112+'+str(int(self.w/2)-131*1)+
                                        '+'+str(int(self.h/2)-56*1))
            self.loadingSplash.update_idletasks()
            self.loadingSplash.update()
        except:
            #log
            pass

    def allocateVars(self):
        #informative
        self.botName = 'SirBot'
        self.botVersion = '0.0.0'

        #queues
        self.chatStack = []
        self.messagelen = []
        self.msgfragments = []
        self.userlisterror = []

        #control variables
        self.geomMain = ''
        self.backgroundColor = '#3496B2'
        self.fontColor = 'black'

        #tk control variables
        self.editConfig = tk.IntVar()
        self.autoMod = tk.IntVar()
        self.childOpen = tk.IntVar()
        self.newChannelName = tk.StringVar()
        self.ownerUpdate = tk.StringVar()
        self.terminalInput = tk.StringVar()
        self.onTop = tk.IntVar()

        self.editConfig.set(0)
        self.autoMod.set(1)
        self.childOpen.set(0)
        self.newChannelName.set('')
        self.ownerUpdate.set('')
        self.terminalInput.set('')
        self.onTop.set(0)


        #tk user variables
        self.channel = tk.StringVar()
        self.owner = tk.StringVar()
        self.password = tk.StringVar()
        self.users = tk.StringVar()

        #master user list
        self.using = []
        
        self.users.set('1v13G4_DEATH oddba11 whiskerzzzzzzzzzzzzzzzzxyz dopey a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 00')
        

    def createMainWindow(self):
        self.MainWindow = tk.Tk()
        self.MainWindow.geometry('1x1+0+0')
        self.MainWindow.overrideredirect(True)

    def loadMainWindow(self):
        self.MainWindow.overrideredirect(False)
        self.MainWindow.geometry(self.geomMain)
        self.MainWindow.title(self.botName+' v'+self.botVersion)
        self.createTerminalSIMPLE()

        top=self.MainWindow.winfo_toplevel()
        #top.rowconfigure(0,weight=1)
        top.rowconfigure(1,weight=1)
        top.columnconfigure(0,weight=1)
        #top.columnconfigure(1,weight=1)

        self.terminalFrame.rowconfigure(0,weight=1)
        #self.usersListFrame.rowconfigure(1,weight=1)
        self.terminalFrame.columnconfigure(0,weight=1)
        #self.usersListFrame.columnconfigure(1,weight=1)

    def createChildren(self):
        self.createUsersList()
        self.createOptionsMenu()


    def createTerminalSIMPLE(self):
        self.mainHeading = tk.Frame(self.MainWindow,bg=self.backgroundColor)
        self.mainHeading.grid(in_=self.MainWindow,row=0,column=0,sticky='NSEW')
        try:
            self.mainLogo = tk.Label(self.mainHeading,image=self.logoimage,
                                     borderwidth=0)
            self.mainLogo.grid(in_=self.mainHeading,row=0,column=0,sticky='NSW')
        except:
            self.mainLogo = tk.Label(self.mainHeading,text='SirBot',borderwidth=0,
                                     bg=self.backgroundColor)
            self.mainLogo.grid(in_=self.mainHeading,row=0,column=0,sticky='NSW')

        try:
            self.usersButton = tk.Button(self.mainHeading,image=self.usersimage,
                                         bd=0,bg=self.backgroundColor,
                                         activebackground=self.backgroundColor,
                                         highlightbackground=self.backgroundColor,
                                         command=self.showUsers)
            self.usersButton.grid(in_=self.mainHeading,row=0,column=4,sticky='NSE')
        except:
            self.usersButton = tk.Button(self.mainHeading,text='User List',bd=0,
                                         bg=self.backgroundColor,
                                         activebackground=self.backgroundColor,
                                         highlightbackground=self.backgroundColor,
                                         command=self.showUsers)
            self.usersButton.grid(in_=self.mainHeading,row=0,column=4,sticky='NSE')

        try:
            self.optionsButton = tk.Button(self.mainHeading,image=self.optionsimage,
                                           bd=0,bg=self.backgroundColor,
                                           overrelief=tk.FLAT,relief=tk.FLAT,
                                           highlightbackground=self.backgroundColor,
                                           activebackground=self.backgroundColor,
                                           command=self.showOptions)
            self.optionsButton.grid(in_=self.mainHeading,row=0,column=3,sticky='NSE')
        except:
            self.optionsButton = tk.Button(self.mainHeading,text='Options',
                                           bd=0,bg=self.backgroundColor,
                                           highlightbackground=self.backgroundColor,
                                           activebackground=self.backgroundColor,
                                           command=self.showOptions)
            self.optionsButton.grid(in_=self.mainHeading,row=0,column=3,sticky='NSE')
     

        self.mainHeading.columnconfigure(2,weight=1)    
        
        self.terminalFrame = tk.Frame(self.MainWindow,padx=8,pady=8,bg=self.backgroundColor)
        self.terminalFrame.grid(in_=self.MainWindow,row=1,column=0,sticky='NSEW')
        self.createTerminalHistory()
        self.createTerminalInput()

    def createTerminalInput(self):
        self.terminalEntry = ttk.Entry(self.terminalFrame,cursor='xterm',
                                       textvariable=self.terminalInput)
        self.terminalEnter = ttk.Button(self.terminalFrame,text='Enter',
                                        command=self.enterTextBttn)

        self.terminalEntry.bind("<Return>",self.enterText)

        self.terminalEntry.grid(in_=self.terminalFrame,row=1,column=0,sticky='EW',
                                columnspan=11)
        self.terminalEnter.grid(in_=self.terminalFrame,row=1,column=11,sticky='EW',
                                columnspan=2)
        

    def createTerminalHistory(self):
        self.terminalScroll = ttk.Scrollbar(self.terminalFrame,
                                            orient=tk.VERTICAL)
        self.terminalHistory = tk.Text(self.terminalFrame,bg='white',fg='black',
                                   height=32,width=75,takefocus=0,
                                   state='disabled',
                                   yscrollcommand=self.terminalScroll.set)
        self.terminalScroll['command'] = self.terminalHistory.yview
        
        

        self.terminalHistory.grid(in_=self.terminalFrame,row=0,column=0,sticky='NSEW',
                                  columnspan=12)
        self.terminalScroll.grid(in_=self.terminalFrame,row=0,column=12,sticky='NSW')
        
    def createUsersList(self):
        self.UsersList = tk.Toplevel(self.MainWindow)
        self.UsersList.withdraw()
        self.UsersList.title('User List')
        self.UsersList.geometry()

        
        self.usersListHeading = tk.Frame(self.UsersList,bg=self.backgroundColor,
                                         padx=4,pady=4)
        self.usersListHeading.grid(in_=self.UsersList,row=0,column=0,sticky='NSEW')
        try:
            self.usersListHeadingLabel = tk.Label(self.usersListHeading,
                                                  image=self.usersimage,bd=0)
            self.usersListHeadingLabel.grid(in_=self.usersListHeading,row=0,
                                            column=0,sticky='NSW')
        except:
            self.usersListHeadingLabel = tk.Label(self.usersListHeading,
                                                  text='User List',
                                                  bd=0,bg=self.backgroundColor)
            self.usersListHeadingLabel.grid(in_=self.usersListHeading,row=0,
                                            column=0,sticky='NSW')

        self.usersListFrame = tk.Frame(self.UsersList,padx=8,pady=8,bg=self.backgroundColor)
        self.usersListScroll = ttk.Scrollbar(self.usersListFrame,orient=tk.VERTICAL)
        self.usersListText = tk.Listbox(self.usersListFrame,activestyle='dotbox',
                                        cursor='xterm',height=15,
                                        listvariable=self.users,fg=self.fontColor,
                                        yscrollcommand=self.usersListScroll.set)

        self.usersListScroll['command'] = self.usersListText.yview

        self.usersListFrame.grid(in_=self.UsersList,column=0,row=1,sticky='NSEW')
        self.usersListScroll.grid(in_=self.usersListFrame,row=0,column=1,sticky='NSWE')
        self.usersListText.grid(in_=self.usersListFrame,row=0,column=0,sticky='NSEW')

        top=self.UsersList.winfo_toplevel()
        #top.rowconfigure(0,weight=1)
        top.rowconfigure(1,weight=1)
        top.columnconfigure(0,weight=1)
        #top.columnconfigure(1,weight=1)

        self.usersListFrame.rowconfigure(0,weight=1)
        #self.usersListFrame.rowconfigure(1,weight=1)
        self.usersListFrame.columnconfigure(0,weight=1)
        #self.usersListFrame.columnconfigure(1,weight=1)

        self.UsersList.geometry('1x1+0+0')
        self.UsersList.protocol("WM_DELETE_WINDOW",self.hideUsers)

        self.UsersList.update()
        self.UsersList.update_idletasks()
        

    def createOptionsMenu(self):
        self.OptionsMenu = tk.Toplevel(self.MainWindow)
        self.OptionsMenu.withdraw()
        self.OptionsMenu.title('Options')
        self.OptionsMenu.geometry()

        self.optionsMenuHeading = tk.Frame(self.OptionsMenu,bg=self.backgroundColor,
                                         padx=4,pady=4)
        self.optionsMenuHeading.grid(in_=self.OptionsMenu,row=0,column=0,sticky='NSEW')
        try:
            self.optionsMenuHeadingLabel = tk.Label(self.optionsMenuHeading,
                                                  image=self.optionsimage,bd=0)
            self.optionsMenuHeadingLabel.grid(in_=self.optionsMenuHeading,row=0,
                                            column=0,sticky='NSW')
        except:
            self.optionsMenuHeadingLabel = tk.Label(self.optionsMenuHeading,
                                                  text='Options',
                                                  bd=0,bg=self.backgroundColor)
            self.optionsMenuHeadingLabel.grid(in_=self.optionsMenuHeading,row=0,
                                            column=0,sticky='NSW')

        self.OptionsMenu.columnconfigure(0,weight=1)

        self.OptionsMenu.geometry('1x1+0+0')

        self.OptionsMenu.protocol("WM_DELETE_WINDOW",self.hideOptions)

        self.OptionsMenu.update()
        self.OptionsMenu.update_idletasks()
        
    def createTEMP(self):
        self.Main = ttk.Frame(self.MainWindow)
        self.button = ttk.Button(self.Main,text='Button')

        self.Main.grid()
        self.button.grid(sticky='NSEW')

    def enterTextBttn(self):
        inputData = self.terminalEntry.get()
        self.terminalEntry.delete(0,tk.END)
        self.terminalEntry.focus_set()


    def enterText(self,event):
        self.enterTextBttn()

    def showUsers(self):
        self.MainWindow.update_idletasks()
        self.geomMain = self.MainWindow.geometry()
        h=self.geomMain.split('x')
        w=int(h[0])
        h=h[1].split('+')
        x=int(h[1])
        y=int(h[2])
        h=int(h[0])
        self.UsersList.geometry(str(int(w*(1/4)))+'x'+str(int(h*(3/4)))+
                                '+'+str(x+w+16)+'+'+str(y))
        self.UsersList.deiconify()
        self.usersButton['state'] = tk.DISABLED
        self.usersButton.grid_remove()

    def hideUsers(self):
        self.UsersList.withdraw()
        self.usersButton['state'] = tk.NORMAL
        self.usersButton.grid()

    def showOptions(self):
        self.MainWindow.update_idletasks()
        self.geomMain = self.MainWindow.geometry()
        x=self.geomMain.split('+')
        y=x[2]
        x=x[1]
        self.OptionsMenu.geometry('256x256+'+x+'+'+y)
        self.OptionsMenu.deiconify()
        self.optionsButton['state'] = tk.DISABLED
        self.optionsButton.grid_remove()

    def hideOptions(self):
        self.OptionsMenu.withdraw()
        self.optionsButton['state'] = tk.NORMAL
        self.optionsButton.grid()
        

app=GUI()

app.MainWindow.mainloop()



##
### explore Tkinter transparency (simplified)
##try:
##    # Python2
##    import Tkinter as tk
##except ImportError:
##    # Python3
##    import tkinter as tk
##root = tk.Tk()
##root.overrideredirect(1)
### use opacity alpha values from 0.0 to 1.0
### opacity/tranparency applies to image and frame
##root.wm_attributes('-alpha', 0.2)  
### use a GIF image you have in the working directory
### or give full path
##photo = tk.PhotoImage(file="Sirbot.gif")
##tk.Label(root, image=photo).pack()
##root.mainloop()


#R:52
#G:150
#B:178
#Hex:3496B2
