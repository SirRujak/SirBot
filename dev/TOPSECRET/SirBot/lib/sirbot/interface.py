# -*- coding: utf-8 -*-

#class containing all graphical user interface elements other than startup splash

import queue #individual imports eventually
import tkinter as tk #individual imports eventually
from tkinter import ttk #individual imports eventually
from sys import platform

class GUI():

    self.geomMain = '621x541+50+50'
    
    def createMainWindow(self):
        self.MainWindow = tk.Tk()
        self.MainWindow.withdraw()
        try:
            if(platform=='win32'):
                self.MainWindow.iconbitmap(default='SirBot.ico')
            else:
                self.tk.call('wm', 'iconphoto', str(root), "-default", *icons)
        except:
            #log
            pass
        self.MainWindow.overrideredirect(True)
        self.MainWindow.protocol("WM_DELETE_WINDOW",self.cleanUp)
        self.mainHeading = tk.Frame(self.MainWindow)

    def allocateVars(self):
        #tk control variables
        self.editConfig = tk.IntVar()
        self.autoMod = tk.IntVar()
        self.childOpen = tk.IntVar()
        self.newChannelName = tk.StringVar()
        self.ownerUpdate = tk.StringVar()
        self.terminalInput = tk.StringVar()
        self.onTop = tk.IntVar()
        self.rawChat = tk.IntVar()

        self.editConfig.set(0)
        self.autoMod.set(1)
        self.childOpen.set(0)
        self.newChannelName.set('')
        self.ownerUpdate.set('')
        self.terminalInput.set('')
        self.onTop.set(0)
        self.rawChat.set(self.raw)


        #tk user variables
        self.channel = tk.StringVar()
        self.owner = tk.StringVar()
        self.password = tk.StringVar()
        self.users = tk.StringVar()

    def cleanUp(self):
        self.MainWindow.update()
        self.MainWindow.withdraw()
        self.OptionsMenu.withdraw()
        self.UsersList.withdraw()
        #do tasks
        time.sleep(.5)
        self.MainWindow.destroy()
        

    def loadMainWindow(self):
        self.MainWindow.overrideredirect(False)
        self.MainWindow.geometry(self.geomMain)
        self.MainWindow.deiconify()
        self.MainWindow.title(self.botName+' v'+self.botVersion)
        self.createTerminalSIMPLE()

        top=self.MainWindow.winfo_toplevel()
        top.rowconfigure(1,weight=1)
        top.columnconfigure(0,weight=1)

        self.terminalFrame.rowconfigure(0,weight=1)
        self.terminalFrame.columnconfigure(0,weight=1)

    def createChildren(self):
        self.createUsersList()
        self.createOptionsMenu()
        self.createUsersContextMenu()
        self.createMainHeaderContextMenu()


    def createTerminalSIMPLE(self):
        self.mainHeading['bg'] = self.backgroundColor
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
            self.usersButton = tk.Button(self.mainHeading,image=self.userslistimage,
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
                                   state='disabled',wrap=tk.WORD,
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
                                        selectmode=tk.MULTIPLE,height=15,
                                        listvariable=self.users,fg=self.fontColor,
                                        yscrollcommand=self.usersListScroll.set)

        self.usersListScroll['command'] = self.usersListText.yview

        self.usersListFrame.grid(in_=self.UsersList,column=0,row=1,sticky='NSEW')
        self.usersListScroll.grid(in_=self.usersListFrame,row=0,column=1,sticky='NSWE')
        self.usersListText.grid(in_=self.usersListFrame,row=0,column=0,sticky='NSEW')

        top=self.UsersList.winfo_toplevel()
        top.rowconfigure(1,weight=1)
        top.columnconfigure(0,weight=1)

        self.usersListFrame.rowconfigure(0,weight=1)
        self.usersListFrame.columnconfigure(0,weight=1)

        self.UsersList.geometry('1x1+0+0')
        self.UsersList.protocol("WM_DELETE_WINDOW",self.hideUsers)

        self.UsersList.update()
        self.UsersList.update_idletasks()
        

    def createOptionsMenu(self):
        self.OptionsMenu = tk.Toplevel(self.MainWindow)
        self.OptionsMenu.withdraw()
        self.OptionsMenu.resizable(width=False,height=False)
        self.OptionsMenu.title('Options')
        self.optionsStyle = ttk.Style()
        self.optionsStyle.configure("TNotebook",background=self.backgroundColor,padding=0)
        self.optionsStyle.map("TNotebook.Tab",background=[("selected", 'black')], foreground=[("selected", 'black')])
        self.optionsStyle.configure("TNotebook.Tab", background=self.backgroundColor, foreground='black',padding=0)

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
        self.OptionsMenu.rowconfigure(1,weight=1)

        self.optionsFrame = tk.Frame(self.OptionsMenu,bg=self.backgroundColor,
                                     padx=4,pady=4)
        self.optionsTabs = ttk.Notebook(self.optionsFrame,padding=0)
        self.dashboardTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor,padx=0)

        self.chatTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        self.rawToggle = tk.Radiobutton(self.chatTab,bg=self.backgroundColor,
                                        variable=self.rawChat,text='Raw Chat',
                                        anchor='nw',command=self.toggleRawChat,
                                        value=1)
        
        self.usersTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        self.commandsTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        self.advancedTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        self.helpTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)

        self.optionsFrame.grid(in_=self.OptionsMenu,row=1,column=0,sticky='NSEW')
        self.optionsTabs.pack(fill=tk.BOTH,expand=tk.Y,padx=0,pady=0)
        self.optionsTabs.enable_traversal()

        try:
            self.optionsTabs.add(self.dashboardTab,image=self.dashboardimage,padding=2)
        except:
            #log
            self.optionsTabs.add(self.dashboardTab,text='Dashboard',padding=2)
        try:            
            self.optionsTabs.add(self.chatTab,image=self.chatimage,padding=2)
        except:
            #log
            self.optionsTabs.add(self.chatTab,text='Chat',padding=2)

        self.rawToggle.grid(row=0,column=0)
        try:
            self.optionsTabs.add(self.usersTab,image=self.usersimage,padding=2)
        except:
            #log
            self.optionsTabs.add(self.usersTab,text='Users',padding=2)
        try:
            self.optionsTabs.add(self.commandsTab,image=self.commandsimage,padding=2)
        except:
            #log
            self.optionsTabs.add(self.commandsTab,text='Commands',padding=2)
        try:
            self.optionsTabs.add(self.advancedTab,image=self.advancedimage,padding=2)
        except:
            #log
            self.optionsTabs.add(self.advancedTab,text='Advanced',padding=2)
        try:
            self.optionsTabs.add(self.helpTab,image=self.helpimage,padding=2)
        except:
            #log
            self.optionsTabs.add(self.helpTab,text='Help',padding=2)

        self.OptionsMenu.geometry('1x1+0+0')

        self.OptionsMenu.protocol("WM_DELETE_WINDOW",self.hideOptions)

        self.OptionsMenu.update()
        self.OptionsMenu.update_idletasks()
        
    def createUsersContextMenu(self):
        self.UsersContextMenu=tk.Menu(self.UsersList,tearoff=0)
        self.UsersContextMenu.add_command(label='Ban')
        self.UsersContextMenu.add_separator()
        self.UsersContextMenu.add_command(label='Find...')
        self.UsersContextMenu.add_command(label='Top',command=self.goListTop)
        self.UsersContextMenu.add_command(label='Random')
        self.UsersContextMenu.add_command(label='Select All',command=self.selectAllUsers)
        self.UsersContextMenu.add_command(label='Clear',command=self.clearUserSelection)
        self.UsersContextMenu.add_command(label='More...')
        self.usersListText.bind("<Button-3>",self.usersContext)

    def createMainHeaderContextMenu(self):
        if(platform == 'win32'):
            self.MainHeaderContextMenu=tk.Menu(self.MainWindow,tearoff=0)
            self.MainHeaderContextMenu.add_checkbutton(label='Always on Top',
                                                       variable=self.onTop,
                                                       command=self.alwaysOnTop)
            self.MainHeaderContextMenu.add_separator()
        self.MainHeaderContextMenu.add_command(label='Options',command=self.showOptions)
        self.MainHeaderContextMenu.add_command(label='Help')
        self.mainHeading.bind("<Button-3>",self.mainContext)
        


    def createTEMP(self):
        self.Main = ttk.Frame(self.MainWindow)
        self.button = ttk.Button(self.Main,text='Button')

        self.Main.grid()
        self.button.grid(sticky='NSEW')

    def alwaysOnTop(self):
        if(self.onTop.get() == 1):
            self.MainWindow.wm_attributes("-topmost",1)
            self.UsersList.wm_attributes("-topmost",1)
            self.OptionsMenu.wm_attributes("-topmost",1)
        else:
            self.MainWindow.wm_attributes("-topmost",0)
            self.UsersList.wm_attributes("-topmost",0)
            self.OptionsMenu.wm_attributes("-topmost",0)

    def toggleRawChat(self):
        if(self.rawChat.get() == 0):
            self.raw = 1
        else:
            self.raw = 0

    def enterTextBttn(self):
        self.enterText(0)

    def enterText(self,event):
        message = self.terminalEntry.get()
        if(message != ''):
            inputData = []
            inputData.append(self.timeStamp())
            inputData.append('Input')
            inputData.append(': ')
            inputData.append(message)
            inputData.append(0)
            self.inputqueue.put(inputData)
            self.terminalEntry.delete(0,tk.END)
            self.writeInput()
            self.parseCommands(inputData)
            self.terminalEntry.focus_set()


    def writeInput(self):
        data = self.inputqueue.get()
        if(data[4] == 0):
            #this will be irc.styleChat(data) or similar
            data = self.styleChat(data)
            self.displayToTerminal(data[0],(data[1],'Time'))
            self.displayToTerminal(data[1],(data[1]))
            self.displayToTerminal(data[2],(data[1],'Text'))
            self.displayToTerminal(data[3],(data[1],'Text'))
            self.displayToTerminal('\n',(data[1]))
        else:
            #extend [data[]] by extra tags and convert to tuple
            tag = [data[1]]
            tag.extend(data[4])
            tag.append('Time')
            tags = tuple(tag)
            self.displayToTerminal(data[0],tags)
            tag.pop()
            tags = tuple(tag)
            self.displayToTerminal(data[1],tags)
            tag.append('Text')
            tags = tuple(tag)
            self.displayToTerminal(data[2],tags)
            self.displayToTerminal(data[3],tags)
            tag.pop()
            tags = tuple(tag)
            self.displayToTerminal('\n',tags)
            
        self.MainWindow.update()

    def writeInputRAW(self):
        data = self.inputqueue.get()
        self.displayToTerminal(data,'Raw')
        self.displayToTerminal('\n','Raw')

    def sendOutput(self,data):
        self.outputqueue.put(data[3])
        
    def showUsers(self):
        self.MainWindow.update_idletasks()
        self.geomMain = self.MainWindow.geometry()
        h=self.geomMain.split('x')
        w=int(h[0])
        h=h[1].split('+')
        x=int(h[1])
        y=int(h[2])
        h=int(h[0])
        if(x+w+16+(1/4)*w <= self.w):
            self.UsersList.geometry(str(int(w*(1/4)))+'x'+str(int(h*(3/4)))+
                                    '+'+str(x+w+16)+'+'+str(y))
        else:
            self.UsersList.geometry(str(int(w*(1/4)))+'x'+str(int(h*(3/4)))+
                                    '+'+str(x-int((1/4)*w)-16)+'+'+str(y))
        self.UsersList.deiconify()
        self.usersButton['state'] = tk.DISABLED
        self.usersButton.grid_remove()
        self.MainWindow.update()

    def hideUsers(self):
        self.UsersList.withdraw()
        self.usersButton['state'] = tk.NORMAL
        self.usersButton.grid()
        self.MainWindow.update()

    def showOptions(self):
        self.MainWindow.update_idletasks()
        self.geomMain = self.MainWindow.geometry()
        x=self.geomMain.split('+')
        y=x[2]
        x=x[1]
        self.OptionsMenu.geometry('540x420+'+x+'+'+y)
        self.OptionsMenu.deiconify()
        self.optionsButton['state'] = tk.DISABLED
        self.optionsButton.grid_remove()
        self.MainWindow.update()

    def hideOptions(self):
        self.OptionsMenu.withdraw()
        self.optionsButton['state'] = tk.NORMAL
        self.optionsButton.grid()
        self.MainWindow.update()


    def usersContext(self,event):
        self.UsersContextMenu.tk_popup(event.x_root,event.y_root,0)
        temp=(self.usersListText.get(self.usersListText.nearest(event.y)))

    def mainContext(self,event):
        self.MainHeaderContextMenu.tk_popup(event.x_root,event.y_root,0)
        

    def goListTop(self):
        self.usersListText.see(0)
        self.setUsers()

    def selectAllUsers(self):
        self.usersListText.selection_set(0,tk.END)

    def clearUserSelection(self):
        self.usersListText.selection_clear(0,tk.END)

    def displayToTerminal(self,data,tag=None):
        self.terminalHistory.config(state='normal')
        try:
            self.terminalHistory.insert(tk.END,data,tag)
        except tk._tkinter.TclError:
            tags = list(tag)
            tags.append('Error')
            tag = tuple(tags)
            self.terminalHistory.insert(tk.END,"<Unable to display text>",tag)
        self.terminalHistory.tag_config('Time',foreground='grey')
        self.terminalHistory.tag_config('Input',foreground='red')
        self.terminalHistory.tag_config('User',foreground='red')
        self.terminalHistory.tag_config('Text',foreground='black')
        self.terminalHistory.yview(tk.END)
        self.terminalHistory.config(state='disabled')

    def incomingMessage(self,message):
        if(self.raw == 0):
            data = self.extractChat(message,self.timeStamp())
            self.inputqueue.put(data)
            self.writeInput()
        else:
            #not until parser works with other modes:
            #temp = self.extractChat(message,self.timeStamp())
            data = message
            self.inputqueue.put(data)
            self.writeInputRAW()


    def addColor(self,color):
        #add possible font color to database if not already present. set user color if not overriden by a default
        pass

    def setUsers(self):
        self.users.set(" ".join(self.using).strip('[').strip(']').replace(','," "))

    def terminalOutput(self,message):
        if(message != ''):
            inputData = []
            inputData.append(self.timeStamp())
            inputData.append('Console')
            inputData.append(': ')
            inputData.append(message)
            inputData.append(['Raw'])
            self.inputqueue.put(inputData)
            self.writeInput()
        
