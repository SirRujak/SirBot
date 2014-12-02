# -*- coding: utf-8 -*-

try:
    import queue
    import time
    import tkinter as tk

    from tkinter import ttk

    from sys import platform

except ImportError:
    print("Unable to import one of: queue, time, tkinter, platform")

class interface():

    def __init__(self,config,assets,interinput,interoutput,root=None):
        self.launch(root,config,assets,interinput,interoutput)
        self.alt=1#temporary

    def display(self):
        self.geomMain = self.config['Interface']['map']
        self.loadMainWindow()
        self.MainWindow.update()
        self.MainWindow.update_idletasks()

    def tick(self):
        self.alt=self.alt*(-1)#temporary
        if(self.alt==1):#temporary
            self.MainWindow.update_idletasks()
        try:
            temp = self.inputqueue.get_nowait()
            if(temp[0] == 24):
                self.writeInput(temp[1])
            elif(temp[0] == 25):
                self.updateConfig(temp[1])
            elif(temp[0] == 26):
                self.updateIRCData(temp[1])
        except queue.Empty:
            pass
        self.MainWindow.update()
        return(self.status)

    def launch(self,root,config,assets,interinput,interoutput):
        self.createMainWindow(root)
        self.imports(assets)       
        self.allocateVars(config,interinput,interoutput)
        self.createChildren()
        self.style()
        
    def style(self):
        self.mainStyle = ttk.Style()
        self.mainStyle.theme_create('Sirbot',parent='default',settings={
            ".": {
                "configure":{
                    "background":self.backgroundColor,
                    "troughcolor":'#A8DDE7',
                    #"fieldbackground":'white',
                    #"font":"",
                    "borderwidth":0}},
            "TLabel":{
                "configure":{
                    'padding':[0,0,0,0],
                    'borderwidth':0}
                },
            

            
            "Vertical.TScrollbar": {
                "layout":[
                    ("Vertical.Scrollbar.uparrow",{"side":"top","sticky":''}),
                    ("Vertical.Scrollbar.downarrow",{"side":"bottom","sticky":''}),
                    ("Vertical.Scrollbar.trough",{"sticky":"ns","children":[
                        ("Vertical.Scrollbar.thumb",{"expand":1,"unit":1,
                                                     "children":[
                                                         ("Vertical.Scrollbar.grip",{
                                                             "sticky":''})]})]})],
                "configure":{
                    "background":'#5CC6DE',
                    "troughcolor":'#A8DDE7',
                    "borderwidth":0},
                "map":{
                    "background":[("active",'#5CC6DE')]}
                },

            "Scrollbar.downarrow": {"element create":
                ("image", self.dwn,
                ("pressed", self.dwn2), {'sticky': ''})
            },

            "Scrollbar.uparrow":{"element create":
                                 ("image",self.up,
                                  ("pressed",self.up2),{'sticky':''})
            },
            
            "TButton":{"element create":
                       ("image",self.enterimage,
                        ("pressed",self.enterimage2),{'sticky':''})
            },

            "Tab":{
                "map":{
                    "expand":[('selected',[0,0,0,4])]},
                
                "layout":[
                    ("Notebook.tab",{'sticky':'nswe','children':
                                     [('Notebook.padding',{
                                         'side':'top','sticky':'nswe',
                                         'children':[
                                             ('Notebook.label',{'side':'top',
                                                               'sticky':''})],
                                         })]
                                     })]
                },

            "TNotebook":{
                "configure":{
                    "tabmargins":[4,0,4,0],
                    'background':self.backgroundColor}},
            "TNotebook.Tab":{
                "configure":{
                    "padding":[4,4,4,0],
                    "background":'#5CC6DE'},
                "map":{
                    "background":[("selected",'#5CC6DE')]}}
            

            })
        self.mainStyle.theme_use('Sirbot')

    def imports(self,assets):
        try:
            self.logoimage = tk.PhotoImage(file=assets.logoimage)
        except:
            #log
            pass
        try:
            self.userslistimage = tk.PhotoImage(file=assets.userslistimage)
        except:
            #log
            pass
        try:
            self.optionsimage = tk.PhotoImage(file=assets.optionsimage)
        except:
            #log
            pass
        try:
            self.dashboardimage = tk.PhotoImage(file=assets.dashboardimage)
        except:
            #log
            pass
        try:
            self.chatimage = tk.PhotoImage(file=assets.chatimage)
        except:
            #log
            pass
        try:
            self.usersimage = tk.PhotoImage(file=assets.usersimage)
        except:
            #log
            pass
        try:
            self.commandsimage = tk.PhotoImage(file=assets.commandsimage)
        except:
            #log
            pass
        try:
            self.advancedimage = tk.PhotoImage(file=assets.advancedimage)
        except:
            #log
            pass
        try:
            self.helpimage = tk.PhotoImage(file=assets.helpimage)
        except:
            #log
            pass
        try:
            self.dwn = tk.PhotoImage(file=assets.dwn,format="gif89")
            self.dwn2 = tk.PhotoImage(file=assets.dwn2,format="gif89")
            self.up = tk.PhotoImage(file=assets.up,format="gif89")
            self.up2 = tk.PhotoImage(file=assets.up2,format="gif89")
        except:
            #log
            pass
        try:
            self.enterimage = tk.PhotoImage(file=assets.enterimage,format="gif89")
            self.enterimage2 = tk.PhotoImage(file=assets.enterimage2,format="gif89")
        except:
            #log
            pass
        try:
            self.optheader = tk.PhotoImage(file=assets.optheader,format="gif89")
        except:
            #log
            pass
        try:
            if(platform=='win32'):
                item = assets.assetPath+'SirBot.ico'
                self.MainWindow.iconbitmap(default=item)
            else:
                self.tk.call('wm', 'iconphoto', str(root), "-default", *icons)
        except:
            #log
            pass
        
    def allocateVars(self,config,interinput,interoutput):
        self.config = config
        self.status = 1
        self.top = self.MainWindow.winfo_toplevel()
        self.h = self.MainWindow.winfo_screenheight()
        self.w = self.MainWindow.winfo_screenwidth()
        self.currentChannel = self.config['Twitch Channels']['default channel']
        self.speaker = self.config['Twitch Accounts']['automated account']['name']
        
        #informative
        self.botName = 'SirBot'
        self.botVersion = '0.0.0'

        #queues
        self.inputqueue = interinput
        self.outputqueue = interoutput
        self.messagelen = []
        self.msgfragments = []
        self.userlisterror = []

        #control variables
        self.geomMain = ''
        self.backgroundColor = '#3496B2'
        self.fontColor = 'black'
        self.raw = self.config['Interface']['chat']['raw']

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

        #user lists
        self.using = []
        self.viewers = []
        self.groups = []
        self.followers = []
        self.subscribers = []
        self.mods = []
        self.specialusers = []

    def createMainWindow(self,root=None):
        if(root == None):
            from tkinter import Tk
            self.MainWindow = Tk()
        else:
            self.MainWindow = root
            self.MainWindow.withdraw()
        #self.MainWindow.geometry('1x1+0+0')
        self.MainWindow.overrideredirect(True)
        self.MainWindow.wm_attributes('-alpha',1)
        self.MainWindow.protocol("WM_DELETE_WINDOW",self.cleanUp)
        self.mainHeading = tk.Frame(self.MainWindow)

    def cleanUp(self):
        self.MainWindow.update()
        self.MainWindow.update_idletasks()
        self.config['Interface']['map'] = self.MainWindow.geometry()
        self.MainWindow.withdraw()
        self.OptionsMenu.withdraw()
        self.UsersList.withdraw()
        #do tasks - save queue members
        self.outputqueue.put([25,0])
        self.status = 0
    
    def shutdown(self):
        self.MainWindow.destroy()

    def loadMainWindow(self):
        self.MainWindow.overrideredirect(False)
        self.MainWindow.geometry(self.geomMain)
        self.MainWindow.deiconify()
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
        try:
            self.terminalEnter = ttk.Button(self.terminalFrame,image=self.enterimage,
                                            command=self.enterText)
        except:
            self.terminalEnter = ttk.Button(self.terminalFrame,text='Enter',
                                            command=self.enterText)

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
                                       relief=tk.FLAT,
                                       yscrollcommand=self.terminalScroll.set)
        self.terminalScroll['command'] = self.terminalHistory.yview
        
        

        self.terminalHistory.grid(in_=self.terminalFrame,row=0,column=0,sticky='NSEW',
                                  columnspan=12)
        self.terminalScroll.grid(in_=self.terminalFrame,row=0,column=12,sticky='NSW')
        
    def createUsersList(self):
        self.UsersList = tk.Toplevel(self.MainWindow)
        self.UsersList.withdraw()
        self.UsersList.title('User List')
        #self.UsersList.geometry()

        
        self.usersListHeading = tk.Frame(self.UsersList,bg=self.backgroundColor,
                                         padx=4,pady=4)
        self.usersListHeading.grid(in_=self.UsersList,row=0,column=0,sticky='NSEW')
        try:
            self.usersListHeadingLabel = tk.Label(self.usersListHeading,
                                                  image=self.userslistimage,bd=0)
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
        self.OptionsMenu.resizable(width=False,height=False)
        self.OptionsMenu.title('Options')

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
                                     padx=0,pady=0)
        self.optionsTabs = ttk.Notebook(self.optionsFrame,padding=0)
        self.dashboardTab = ttk.Frame(self.optionsTabs)
#        try:
        self.dashboardLabel=ttk.Label(self.dashboardTab,image=self.optheader)
#        except:
            #log
#            pass
        self.chatTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        try:
            self.chatLabel=ttk.Label(self.chatTab,image=self.optheader)
        except:
            #log
            pass
        self.rawToggle = tk.Checkbutton(self.chatTab,bg=self.backgroundColor,
                                        variable=self.rawChat,text='Raw Chat',
                                        anchor='nw',command=self.toggleRawChat)
        
        self.usersTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        try:
            self.usersLabel=ttk.Label(self.usersTab,image=self.optheader)
        except:
            #log
            pass
        
        self.commandsTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        try:
            self.commandsLabel = ttk.Label(self.commandsTab,image=self.optheader)
        except:
            #log
            pass
        
        self.advancedTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        try:
            self.advancedLabel = ttk.Label(self.advancedTab,image=self.optheader)
        except:
            #log
            pass
        
        self.helpTab = tk.Frame(self.optionsTabs,bg=self.backgroundColor)
        try:
            self.helpLabel = ttk.Label(self.helpTab,image=self.optheader)
        except:
            #log
            pass
        
        self.optionsFrame.grid(in_=self.OptionsMenu,row=1,column=0,sticky='NSEW')
        #self.optionsFrame.row
        self.optionsTabs.pack(fill=tk.BOTH,expand=tk.Y,padx=0,pady=0)
        self.optionsTabs.enable_traversal()

        try:
            self.optionsTabs.add(self.dashboardTab,image=self.dashboardimage,padding=2)
            self.dashboardLabel.grid(row=0,column=0)
        except:
            #log
            self.optionsTabs.add(self.dashboardTab,text='Dashboard',padding=0)
        try:            
            self.optionsTabs.add(self.chatTab,image=self.chatimage,padding=2)
            self.chatLabel.grid(row=0,column=0)
        except:
            #log
            self.optionsTabs.add(self.chatTab,text='Chat',padding=0)
        self.rawToggle.grid(row=1,column=0,sticky='W')
        try:
            self.optionsTabs.add(self.usersTab,image=self.usersimage,padding=2)
            self.usersLabel.grid(row=0,column=0)
        except:
            #log
            self.optionsTabs.add(self.usersTab,text='Users',padding=2)
        try:
            self.optionsTabs.add(self.commandsTab,image=self.commandsimage,padding=2)
            self.commandsLabel.grid(row=0,column=0)
        except:
            #log
            self.optionsTabs.add(self.commandsTab,text='Commands',padding=2)
        try:
            self.optionsTabs.add(self.advancedTab,image=self.advancedimage,padding=2)
            self.advancedLabel.grid(row=0,column=0)
        except:
            #log
            self.optionsTabs.add(self.advancedTab,text='Advanced',padding=2)
        try:
            self.optionsTabs.add(self.helpTab,image=self.helpimage,padding=2)
            self.helpLabel.grid(row=0,column=0)
        except:
            #log
            self.optionsTabs.add(self.helpTab,text='Help',padding=2)

##        self.OptionsMenu.geometry('1x1+0+0')

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
        if(self.rawChat.get() == 1):
            #self.raw = 1
            #send command to application.py to change raw setting
            pass
        else:
            #self.raw = 0
            #same as above
            pass

    def timeStamp(self):
        times = time.asctime(time.localtime(time.time()))
        times = times[11:19]
        times = '['+times+']'
        return times

    def enterTextBttn(self):
        #deprecated
        self.enterText(0)
        

    def enterText(self,event=None):
        message = self.terminalEntry.get()
        if(message != ''):
            inputData = []
            inputData.append(self.timeStamp())
            inputData.append('['+self.currentChannel+']')
            inputData.append(self.speaker)
            inputData.append(':')
            inputData.append(message)
            inputData.append(0)
##            self.inputqueue.put(inputData)
            self.terminalEntry.delete(0,tk.END)
            self.writeInput(inputData)
            self.sendOutput(message)
            self.terminalEntry.focus_set()


    def writeInput(self,data):
        if(data[5] == 0):
            data = self.styleChat(data)
            self.displayToTerminal(data[0],(data[1],data[2],'Time'))
            self.displayToTerminal(data[1],(data[1],data[2],'Channel'))
            self.displayToTerminal(data[2],(data[1],data[2]))
            self.displayToTerminal(data[3],(data[1],data[2],'Text'))
            self.displayToTerminal(data[4],(data[1],data[2],'Text'))
            self.displayToTerminal('\n',(data[1],data[2]))
        else:
            #extend [data[]] by extra tabs and convert to tuple
            tag = data[1:2]
            tag.extend(data[5])
            tag.append('Time')
            tags = tuple(tag)
            self.displayToTerminal(data[0],tags)
            tag.pop()
            tag.append('Channel')
            tags = tuple(tag)
            self.displayToTerminal(data[1],tags)
            tag.pop()
            tags = tuple(tag)
            self.displayToTerminal(data[2],tags)
            tag.append('Text')
            tags = tuple(tag)
            self.displayToTerminal(data[3],tags)
            self.displayToTerminal(data[4],tags)
            tag.pop()
            tags = tuple(tag)
            self.displayToTerminal('\n',tags)
            

    def writeInputRAW(self):
        try:
            data = self.inputqueue.get_nowait()
            self.displayToTerminal(data,'Raw')
            self.displayToTerminal('\n','Raw')
        except queue.Empty:
            pass


    def sendOutput(self,data):
        self.outputqueue.put([2,data])
        

    def styleChat(self,data):
        #consider implementing a tag for actions- would need low priority
        if(data[1] is not 'Server'):
            data[3] = data[3].replace("\\'","'")
            data[3] = data[3].replace("', '",":")
            data[3] = data[3].replace('", "',":")
            data[3] = data[3].replace('''', "''',":")
            data[3] = data[3].replace("""", '""",":")
            if("\\x01ACTION" in data[3]):
                data[3] = data[3].replace("\\x01ACTION",'')
                data[3] = data[3].replace("\\x01",'')
                data[2] = ''
        return(data)

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
        self.OptionsMenu.geometry('640x480+'+x+'+'+y)
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
        #self.terminalHistory.tag_config('Input',foreground='red')
        #self.terminalHistory.tag_config('Input',elide=1)
        #self.terminalHistory.tag_config('User',foreground='red')
        self.terminalHistory.tag_config('Text',foreground='black')
        self.terminalHistory.tag_config('Info',elide=1)
        self.terminalHistory.tag_config('Channel',elide=1)
        #print(self.terminalScroll.get())
        #print(tk.END)
        if(self.terminalScroll.get()[1]==1.0):
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

    def setUsers(self,data):
        self.users.set(" ".join(data).strip('[').strip(']').replace(','," "))

    def updateConfig(self,data):
        pass

    def updateIRCData(self,data):
        if(data[0] == 'users'):
            self.setUsers(data[1])
            #print(data[1])



if __name__ == "__main__":
    temp1=queue.Queue()
    temp2=queue.Queue()
    cfg={}
    #
    app=interface(cfg,assets,temp1,temp2)
    app.MainWindow.mainloop()


#tags:
#input/*username*/server/console/channel
#time/text

#/join/part/welcome/users/ping/mods/info/error/recovered/raw

#['<timestamp>','[channel]','<input/*username*/server/console>',':','<message>',[<extra-tags>]]



##import tkinter as tk
##
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
