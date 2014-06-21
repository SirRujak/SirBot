#

import tkinter as tk

botName = 'Nombot'
botVersion = '0.0.*'
msgID = 'Console:'
defaultState = 1

class botGUI(tk.Frame):
    def __init__(self,master=None):

        tk.Frame.__init__(self,master)

        self.grid()
        self.createWidgets()

    #global class variables
        

    def createWidgets(self):

        ##status variables

        #user variables
        self.autoMod = tk.IntVar()
        self.channel = tk.StringVar()
        self.owner = tk.StringVar()
        self.users = tk.StringVar()

        self.autoMod.set(defaultState)
        self.users.set('1v13G4_DEATH oddba11 whiskerzzzzzzzzzzzzzzzzxyz dopey a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 00')
        self.owner.set('id')
        self.channel.set('MINE')

        #active IRC users declare
        self.statusFrame = tk.LabelFrame(self,labelanchor='nw',text='Status')
        self.channelFrame = tk.LabelFrame(self,labelanchor='nw',text='Current Channel')
        self.channelName = tk.Label(self,bg='white',fg='black',textvariable=self.channel)
        self.usersFrame = tk.Frame(self,background='white')
        self.sendAs = tk.LabelFrame(self,labelanchor='nw',text='Send As:')
        self.sendAsText = tk.Label(self,bg='white',fg='black',textvariable=self.owner)
        self.usersList = tk.LabelFrame(self,labelanchor='nw',text='Users')
        self.usersScroll = tk.Scrollbar(self,orient=tk.VERTICAL)
        self.usersListText = tk.Listbox(self,activestyle='dotbox',bg='white',cursor='xterm',fg='black',height=15,listvariable=self.users,yscrollcommand=self.usersScroll.set)
        
        #active IRC users add to grid
        self.statusFrame.grid(column=0,row=1,sticky='NSEW')
        self.channelFrame.grid(in_=self.statusFrame,row=0,sticky='EW')
        self.channelName.grid(in_=self.channelFrame,sticky='EW')
        self.usersFrame.grid(in_=self.statusFrame,row=1,sticky='EW')
        self.sendAs.grid(in_=self.usersFrame,row=0,sticky='EW')
        self.sendAsText.grid(in_=self.sendAs,sticky='EW')
        self.usersList.grid(in_=self.usersFrame,row=1,sticky='EW')
        self.usersListText.grid(in_=self.usersList,row=0,column=0,sticky='EW')
        self.usersScroll.grid(in_=self.usersList,row=0,column=1,sticky='NS')
        self.usersScroll['command'] = self.usersListText.yview

        #add more status widgets


        #chat variables
        self.chatInput = tk.StringVar()
        ###self.timeStamp = tk.StringVar()

        ###self.timeStamp.set('[00/00/00|00:00:00]')
        #self.timeStamp = '[00:00:00]'

        
        #chat window declare
        self.textFrame = tk.LabelFrame(self,labelanchor='nw',text='Text Interface')
        self.chatFrame = tk.Frame(self)
        self.chatScroll = tk.Scrollbar(self,orient=tk.VERTICAL)
        self.chatHistory = tk.Text(self,bg='white',fg='black',height=32,width=75,takefocus=0,state='disabled',yscrollcommand=self.chatScroll.set)
        self.chatInput = tk.Entry(self,bg='white',fg='black',cursor='xterm',textvariable=self.chatInput)
        self.cmdVerifyButton = tk.Button(self,text='...',command=self.verifyCommand)
        self.chatSendButton = tk.Button(self,text='Send',command=self.sendChat)
        self.chatInput.bind("<Return>",self.sendChat2)
        
        #chat window add to grid
        self.textFrame.grid(column=1,row=1,sticky='NSEW')
        self.chatFrame.grid(in_=self.textFrame,sticky='EW')
        self.chatHistory.grid(in_=self.chatFrame,row=0,column=0,columnspan=4,sticky='EW')
        self.chatScroll.grid(in_=self.chatFrame,row=0,column=4,sticky='NS')
        self.chatInput.grid(in_=self.chatFrame,row=1,column=0,columnspan=3,sticky='EW')
        self.cmdVerifyButton.grid(in_=self.chatFrame,row=1,column=4)
        self.chatSendButton.grid(in_=self.chatFrame,row=1,column=3,columnspan=1,sticky='EW')
        self.chatScroll['command'] = self.chatHistory.yview
        
        #menu bar
        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar
        #menu bar items
        self.runMenu = tk.Menu(self.menuBar)
        self.chatMenu = tk.Menu(self.menuBar)
        self.optionsMenu = tk.Menu(self.menuBar)
        self.helpMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Run',menu=self.runMenu)
        self.menuBar.add_cascade(label='Chat',menu=self.chatMenu)
        self.menuBar.add_cascade(label='Options',menu=self.optionsMenu)
        self.menuBar.add_cascade(label='Help',menu=self.helpMenu)
        self.optionsMenu.add_command(label='Quit',command=self.destroy)
        self.helpMenu.add_command(label='About',command=self.refreshUsers)
        self.helpMenu.add_command(label='Help',command=self.refreshUsers)

        #users context menu
        self.usersContext = tk.Menu(self,tearoff=0)
        self.usersContext.add_command(label="Block")
        self.usersContext.add_command(label='Promote')
        self.usersContext.add_command(label='Demote')
        self.usersContext.add_separator()
        self.usersContext.add_command(label="More..")
        self.usersListText.bind("<Button-3>",self.contextMenu)

        #users list buttons container
        self.usersListButtons = tk.Frame(self,relief=tk.FLAT)
        self.usersListButtons.grid(in_=self.statusFrame,column=0,row=2)

        #user selection buttons
        self.usersSelectionButtons = tk.LabelFrame(self,text='Selection',relief=tk.GROOVE)
        self.usersSelectionButtons.grid(in_=self.usersListButtons,column=0,row=1)

        #user navigation buttons container
        self.userNavigationButtons = tk.Frame(self,relief=tk.FLAT)
        self.userNavigationButtons.grid(in_=self.usersListButtons,column=0,row=0)

        #find user button
        self.findUserButton = tk.Button(self,text='Find',command=self.goToUser)
        self.findUserButton.grid(in_=self.userNavigationButtons,column=0,row=0)

        #top of list button
        self.listTopButton = tk.Button(self,text='Return to Top',command=self.goListTop)
        self.listTopButton.grid(in_=self.userNavigationButtons,column=1,row=0)

        #select all button
        self.userSelectButton = tk.Button(self,text='All',command=self.selectAllUsers)
        self.userSelectButton.grid(in_=self.usersSelectionButtons,column=0,row=0)

        #clear selection button
        self.userDeselectButton = tk.Button(self,text='Clear',command=self.clearUserSelection)
        self.userDeselectButton.grid(in_=self.usersSelectionButtons,column=1,row=0)

        #bot on and off and custom
        self.modAutomation = tk.LabelFrame(self,labelanchor='nw',text='Automated Moderator')
        self.activateAutomation = tk.Radiobutton(self,text='On',value=1,variable=self.autoMod,relief=tk.GROOVE)
        self.deactivateAutomation = tk.Radiobutton(self,text='Off',value=0,variable=self.autoMod,relief=tk.GROOVE)
        self.customAutomation = tk.Button(self,text='Custom',command=self.refreshUsers,relief=tk.GROOVE)
        
        self.modAutomation.grid(in_=self.statusFrame,column=0,row=3)
        self.activateAutomation.grid(in_=self.modAutomation,column=0,row=0)
        self.deactivateAutomation.grid(in_=self.modAutomation,column=1,row=0)
        self.customAutomation.grid(in_=self.modAutomation,column=2,row=0)
        
        #temporary refresh button
        self.refreshButton = tk.Button(self,text='VOID',command=self.refreshUsers)

        self.refreshButton.grid(in_=self.statusFrame,column=0,row=4)


    def refreshUsers(self):
        pass

    def sendChat(self):
        self.chatHistory.config(state='normal')
        self.chatHistory.insert(tk.END,self.timeStamp() +msgID+ self.chatInput.get()+"\n")
        self.chatInput.delete(0,tk.END)
        self.chatHistory.yview(tk.END)
        self.chatHistory.config(state='disabled')
        self.chatInput.focus_set()

    def sendChat2(self,event):
        self.chatHistory.config(state='normal')
        self.chatHistory.insert(tk.END,self.timeStamp() +msgID+ self.chatInput.get()+"\n")
        self.chatInput.delete(0,tk.END)
        self.chatHistory.yview(tk.END)
        self.chatHistory.config(state='disabled')
        self.chatInput.focus_set()

    def timeStamp(self):
        #get time and format appropriately
        time = '[00:00:00]'
        return time

    def contextMenu(self,event):
        #try:
            self.usersContext.tk_popup(event.x_root,event.y_root,4)
            print(self.usersListText.get(self.usersListText.nearest(event.y)))
##        finally:
##            self.usersContext.grab_release()

    def goListTop(self):
        self.usersListText.see(0)

    def selectAllUsers(self):
        self.usersListText.selection_set(0,tk.END)

    def clearUserSelection(self):
        self.usersListText.selection_clear(0,tk.END)

    def verifyCommand(self):
        #make command verifier and employ it here
        #maybe do this to verified lines:
        #self.chatInput.insert(tk.END,'>')
        ##temporarily this:
        print(self.autoMod.get())


    def goToUser(self):
        #search for username in list: if it exists, select it; otherwise do nothing(notify?)
        pass

    def updateUserList(self):
        #self.users
        #insert headings for various tiers
        pass
        
    

UI = botGUI()

UI.master.title(botName + ' v.' + botVersion)

UI.mainloop()

