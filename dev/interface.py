#

import time
import tkinter as tk
from tkinter import ttk
#import re
#import tkinter.ttk
#import os


##botName = 'SirBot'
##botVersion = '0.0.*'
##msgID = 'Console:'
##defaultState = 1

class botGUI(tk.Frame):



    def __init__(self,master=None):

        tk.Frame.__init__(self,master)
        self.grid()
        self.createWidgets()


    #global class variables

    botName = ''
    botVersion = ''
    msgID = ''
    defaultState = 1

    #deque someday
    chatStack = []
    messagelen = []
    using = []
    msgfragments = []
    userlisterror = []


    def createWidgets(self):

        ##status variables
        top = self.winfo_toplevel()
        self.editConfig = tk.IntVar()
        self.editConfig.set(0)
        self.autoMod = tk.IntVar()
        self.autoMod.set(self.defaultState)
        self.childOpen = tk.IntVar()
        self.childOpen.set(0)
        self.newChannelName = tk.StringVar()
        self.newChannelName.set('')

        #user variables
        self.channel = tk.StringVar()
        self.owner = tk.StringVar()
        self.ownerUpdate = tk.StringVar()
        self.password = tk.StringVar()
        self.users = tk.StringVar()

        #active IRC declare
        self.statusFrame = tk.LabelFrame(self,labelanchor='nw',text='Status')
        self.channelFrame = tk.LabelFrame(self,labelanchor='nw',text='Current Channel')
        self.channelName = tk.Label(self,bg='white',fg='black',textvariable=self.channel)
        self.channelChange = tk.Button(self,text='Change',command=self.editChannel)
        self.usersFrame = tk.Frame(self,background='white')
        self.sendAs = tk.LabelFrame(self,labelanchor='nw',text='Send As:')
        self.sendAsText = tk.Label(self,bg='white',fg='black',textvariable=self.owner)
        self.sendAsChange = tk.Button(self,text='Change',command=self.configQuery)
        self.usersList = tk.LabelFrame(self,labelanchor='nw',text='Users')
        self.usersScroll = ttk.Scrollbar(self,orient=tk.VERTICAL)
        self.usersListText = tk.Listbox(self,activestyle='dotbox',bg='white',cursor='xterm',fg='black',height=15,listvariable=self.users,yscrollcommand=self.usersScroll.set)

        #active IRC add to grid
        self.statusFrame.grid(column=0,row=1,sticky='NSEW')
        self.channelFrame.grid(in_=self.statusFrame,row=0,sticky='EW')
        self.channelName.grid(in_=self.channelFrame,sticky='EW',column=0,row=0)
        self.channelChange.grid(in_=self.channelFrame,sticky='E',column=1,row=0)
        self.usersFrame.grid(in_=self.statusFrame,row=1,sticky='EW')
        self.sendAs.grid(in_=self.usersFrame,row=0,sticky='EW',column=0)
        self.sendAsText.grid(in_=self.sendAs,sticky='EW',column=0,row=0)
        self.sendAsChange.grid(in_=self.sendAs,sticky='E',column=1,row=0)
        self.usersList.grid(in_=self.usersFrame,row=1,sticky='EW')
        self.usersListText.grid(in_=self.usersList,row=0,column=0,sticky='EW')
        self.usersScroll.grid(in_=self.usersList,row=0,column=1,sticky='NSE')
        self.usersScroll['command'] = self.usersListText.yview

        #add more status widgets


        #chat variables
        self.chatInput = tk.StringVar()

        #chat window declare
        self.textFrame = tk.LabelFrame(self,labelanchor='nw',text='Text Interface')
        self.chatFrame = tk.Frame(self)

        self.terminalFrame = tk.Frame(self)
        self.terminal = ttk.Notebook(self)
        self.chatHistoryFrame = ttk.Frame(self)
        #chathistorywidget
        self.chatScroll = ttk.Scrollbar(self,orient=tk.VERTICAL)
        self.chatHistory = tk.Text(self,bg='white',fg='black',height=32,width=75,takefocus=0,state='disabled',yscrollcommand=self.chatScroll.set)
        self.terminalHistoryFrame = ttk.Frame(self)


        self.terminalScroll = ttk.Scrollbar(self,orient=tk.VERTICAL)
        self.terminalHistory = tk.Text(self,bg='white',fg='black',height=32,width=75,takefocus=0,state='disabled',yscrollcommand=self.terminalScroll.set)
        self.chatInput = tk.Entry(self,bg='white',fg='black',cursor='xterm',textvariable=self.chatInput)
        self.cmdVerifyButton = tk.Button(self,text='...',command=self.verifyCommand)
        self.chatSendButton = tk.Button(self,text='Send',command=self.sendChat)
        self.chatInput.bind("<Return>",self.sendChat2)


        #chat window add to grid
        self.textFrame.grid(column=1,row=1,sticky='NSEW')
        self.chatFrame.grid(in_=self.textFrame,sticky='EW')

        self.terminalFrame.grid(in_=self.chatFrame,row=0,column=0,columnspan=4,sticky='NSEW')
        self.terminal.pack(in_=self.terminalFrame,fill=tk.BOTH,expand=tk.Y,padx=2,pady=3)
        #grid chathistorywidget
        self.chatHistory.grid(in_=self.chatHistoryFrame,row=0,column=0,columnspan=4,sticky='EW')
        self.chatScroll.grid(in_=self.chatHistoryFrame,row=0,column=4,sticky='NS')
        self.terminal.add(self.chatHistoryFrame,text='Chat',padding=2)

        self.terminalHistory.grid(in_=self.terminalHistoryFrame,row=0,column=0,columnspan=4,sticky='EW')
        self.terminalScroll.grid(in_=self.terminalHistoryFrame,row=0,column=4,sticky='NS')
        self.chatInput.grid(in_=self.chatFrame,row=1,column=0,columnspan=3,sticky='EW')
        self.cmdVerifyButton.grid(in_=self.chatFrame,row=1,column=4)
        self.chatSendButton.grid(in_=self.chatFrame,row=1,column=3,columnspan=1,sticky='EW')
        self.chatScroll['command'] = self.chatHistory.yview
        self.terminalScroll['command'] = self.terminalHistory.yview

        self.terminal.add(self.terminalHistoryFrame,text='Terminal',padding=2)

        #menu bar
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
        self.optionsMenu.add_command(label='Configure',command=self.openOptions)
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

        #users list buttons container <- need to fix layout
        self.usersListButtons = tk.Frame(self,relief=tk.FLAT)
        self.usersListButtons.grid(in_=self.statusFrame,column=0,row=2,sticky='EW')

        #user selection buttons
        self.usersSelectionButtons = tk.LabelFrame(self,text='Selection',relief=tk.GROOVE)
        self.usersSelectionButtons.grid(in_=self.usersListButtons,column=0,row=1,sticky='EW')

        #user navigation buttons container
        self.userNavigationButtons = tk.Frame(self,relief=tk.FLAT)
        self.userNavigationButtons.grid(in_=self.usersListButtons,column=0,row=0,sticky='EW')

        #find user button
        self.findUserButton = tk.Button(self,text='Find',command=self.goToUser)
        self.findUserButton.grid(in_=self.userNavigationButtons,column=0,row=0,sticky='EW')

        #top of list button
        self.listTopButton = tk.Button(self,text='Return to Top',command=self.goListTop)
        self.listTopButton.grid(in_=self.userNavigationButtons,column=1,row=0,sticky='EW')

        #select all button
        self.userSelectButton = tk.Button(self,text='All',command=self.selectAllUsers)
        self.userSelectButton.grid(in_=self.usersSelectionButtons,column=0,row=0,sticky='EW')

        #clear selection button
        self.userDeselectButton = tk.Button(self,text='Clear',command=self.clearUserSelection)
        self.userDeselectButton.grid(in_=self.usersSelectionButtons,column=1,row=0)

        #bot on and off and custom
        self.modAutomation = tk.LabelFrame(self,labelanchor='nw',text='Automated Moderator')
        self.activateAutomation = tk.Radiobutton(self,text='On',value=1,variable=self.autoMod,relief=tk.GROOVE)
        self.deactivateAutomation = tk.Radiobutton(self,text='Off',value=0,variable=self.autoMod,relief=tk.GROOVE)
        self.customAutomation = tk.Button(self,text='Custom',command=self.customAutomatedModerator,relief=tk.GROOVE)

        self.modAutomation.grid(in_=self.statusFrame,column=0,row=3)
        self.activateAutomation.grid(in_=self.modAutomation,column=0,row=0)
        self.deactivateAutomation.grid(in_=self.modAutomation,column=1,row=0)
        self.customAutomation.grid(in_=self.modAutomation,column=2,row=0)

        #temporary function test button
        self.refreshButton = ttk.Button(self,text='VOID',command=self.configQuery)
        self.refreshButton.grid(in_=self.statusFrame,column=0,row=4)

        #sort user list button
        self.sortButton = tk.Button(self,text='Sort',command=self.sortUsers)
        self.sortButton.grid(in_=self.usersListButtons,column=0,row=2,sticky='EW')


    def sortUsers(self):
        pass

    def refreshUsers(self):
        pass

    def terminalOutput(self,message):
        msgID = 'Console:'

        self.terminalWrite(msgID,message)

    def terminalInput(self,message):
        #msgID = str(self.identifyChat(message))+':'
        (msgID,message) = self.extractChat(message)
        msgID = str(msgID)
        self.terminalWrite(msgID,message)
        if(msgID != '' and msgID != 'Server:'):
            self.chatWrite(msgID,message)

    def chatInput(self,message):
        (msgID,message)=self.extractChat(message)
        self.terminalWrite(msgID,message)
        self.chatWrite(msgID,message)

    def terminalWrite(self,msgID,message):
        self.terminalHistory.config(state='normal')
        self.terminalHistory.insert(tk.END,self.timeStamp()+msgID+message+'\n')
        self.terminalHistory.yview(tk.END)
        self.terminalHistory.config(state='disabled')

    def chatWrite(self,msgID,message):
        self.chatHistory.config(state='normal')
        self.chatHistory.insert(tk.END,self.timeStamp()+msgID+message+'\n')
        self.chatHistory.yview(tk.END)
        self.chatHistory.config(state='disabled')


    def sendChat(self):
        inputData = self.chatInput.get()
        if(inputData != ''):
            msgID = self.owner.get() + ':'
            self.chatStack.append(inputData)
            self.chatInput.delete(0,tk.END)
            self.chatInput.focus_set()

    def sendChat2(self,event):
        self.sendChat()

    def timeStamp(self):
        times = time.asctime(time.localtime(time.time()))
        times = times[11:19]
        times = '['+times+']'
        return times

    def contextMenu(self,event):
##        try:
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
        self.checkUserMultiplicity()
        print('AutoModON/OFF:'+str(self.autoMod.get()))
        #print('Top window:'+self.createWidgets.top)
        print('IsChildOpen:'+str(self.childOpen.get()))
        print('IsConfiginEdit:'+str(self.editConfig.get()))
        print("Nameslength:"+str(self.messagelen))
        print("Users:"+str(self.using))
        #print('
        
    def goToUser(self):
        #search for username in list: if it exists, select it; otherwise do nothing(notify?)
        pass

    def formatUserList(self):
        #self.users
        #insert headings for various tiers
        pass

    def configQuery(self):
        #popup window to ask for config file info
        if(self.editConfig.get() == 0):
            self.editConfig.set(1)
            #find current config username and set as self.ownerUpdate
            self.configInput = tk.Toplevel()
            self.configInput.title('Configure Account')
            self.configInput.transient(self)
            self.configInput.geometry('+'+str(self.winfo_rootx()+50)+'+'+str(self.winfo_rooty()+50))
            self.inputUserFrame = tk.LabelFrame(self.configInput,text='Owner Account',labelanchor='nw')
            self.inputUser = tk.Entry(self.inputUserFrame,textvariable=self.ownerUpdate,cursor='xterm')
            self.inputOauthFrame = tk.LabelFrame(self.configInput,text='Oauth Password',labelanchor='nw')
            self.inputOauth = tk.Entry(self.inputOauthFrame,textvariable=self.password,cursor='xterm')
            self.getOauthButton = ttk.Button(self.inputOauthFrame,text='Find Oauth',command=self.getOauth)
            self.inputConfigFrame = ttk.Frame(self.configInput)
            self.inputConfigConfirmButton = ttk.Button(self.inputConfigFrame,text='Confirm',command=self.confirmConfigQuery)
            self.inputConfigDiscardButton = ttk.Button(self.inputConfigFrame,text='Discard',command=self.closeConfigQuery)

            self.inputUserFrame.grid(in_=self.configInput,row=0,sticky='EW',columnspan=2)
            self.inputUser.grid(in_=self.inputUserFrame,sticky='EW',columnspan=3)
            self.inputOauthFrame.grid(in_=self.configInput,row=1,sticky='EW',columnspan=2)
            self.inputOauth.grid(in_=self.inputOauthFrame,sticky='EW',columnspan=2,row=0)
            self.getOauthButton.grid(in_=self.inputOauthFrame,sticky='EW',column=2,row=0)
            self.inputConfigFrame.grid(in_=self.configInput,row=2,sticky='E',columnspan=2)
            self.inputConfigConfirmButton.grid(in_=self.inputConfigFrame,column=0,row=0)
            self.inputConfigDiscardButton.grid(in_=self.inputConfigFrame,column=1,row=0)

            self.inputUser.select_range(0,tk.END)
            self.inputUser.focus_set()

            self.configInput.protocol("WM_DELETE_WINDOW",self.closeConfigQuery)

    def navConfigQuery(self):
        #make pressing enter move to the next entry field
        pass

    def confirmConfigQuery(self):
        #make changes to config file with data from entry fields
        self.closeConfigQuery()

    def closeConfigQuery(self):
        self.ownerUpdate.set('')
        self.editConfig.set(0)
        self.configInput.destroy()

    def editChannel(self):
        #tk.messagebox
        if(self.childOpen.get() == 0):
            self.childOpen.set(1)
            self.channelEdit = tk.Toplevel()
            self.channelEdit.title('Join Channel')
            self.channelEdit.transient(self)
            #self.channelEdit.geometry(wxh+x+y)
            #self.channelEdit.geometry("+%d+%d" % (self.winfo_rootx()+50,self.winfo_rooty()+50))
            self.channelEdit.geometry('+'+str(self.winfo_rootx()+50)+'+'+str(self.winfo_rooty()+50))

            self.channelEntry = tk.Entry(self.channelEdit,bg='white',fg='black',cursor='xterm',textvariable=self.newChannelName)
            self.channelEntry.bind("<Return>",self.editChannelClose2)
            self.joinChannelButton = ttk.Button(self.channelEdit,text='Join',command=self.editChannelClose)

            self.channelEntry.grid(row=0,column=0,sticky='EW')
            self.joinChannelButton.grid(row=1,column=0)

            self.channelEntry.focus_set()

            self.channelEdit.protocol("WM_DELETE_WINDOW", self.editChannelCloseWM)

    def openOptions(self):

        if(self.childOpen.get() == 0):
            self.childOpen.set(1)
            self.optionsDialog = tk.Toplevel()
            self.optionsDialog.title('Options')
            self.optionsDialog.transient(self)
            self.optionsDialog.bind("<Escape>",self.optionsDialogClose2)
            #self.optionsDialog.geometry(wxh+x+y)
            self.optionsDialog.geometry('+'+str(self.winfo_rootx()+50)+'+'+str(self.winfo_rooty()+50))


            #self.testButton = tk.Button(self.optionsDialog,text='Close',command=self.optionsDialogClose)
            #self.testButton.pack()

            self.fortrial = tk.Frame(self.optionsDialog)
            self.fortrial.pack(side=tk.TOP,fill=tk.BOTH,expand=tk.Y)
            self.trial = ttk.Notebook(self.fortrial)
            self.trial.pack(fill=tk.BOTH,expand=tk.Y,padx=2,pady=3)
            self.trial.enable_traversal()
            #tab1
            self.trialframe1 = ttk.Frame(self.trial)
            #ADD WIDGETS HERE
            self.trialbutton1=tk.Button(self.trialframe1,text='submenu1')
            self.trialbutton1.grid()
            self.trialframe1.rowconfigure(1,weight=1)
            self.trialframe1.columnconfigure((0,1),weight=1,uniform=1)
            #display tab1
            self.trial.add(self.trialframe1,text='Tab1',padding=2)
            #tab2
            self.trialframe2=ttk.Frame(self.trial)
            self.trialbutton2=ttk.Button(self.trialframe2,text='submenu2')
            self.trialbutton2.grid()
            #add widgets
            self.trial.add(self.trialframe2,text='Tab2')

            #self.trialframe2 = ttk.Frame(self.trial)
            #self.trial.insert(tk.END,self.trialframe2)
            #self.trialframe2.grid()
            #self.trialbutton2=ttk.Button(self.trialframe2,text='testing2')
            #self.trialbutton2.grid()
            #self.trialframe3 = ttk.Frame(self.trial)
            #self.trial.insert(tk.END,self.trialframe3)
            #self.trialframe3.grid()
            #self.trialbutton3=ttk.Button(self.trialframe1,text='testing3')
            #self.trialbutton3.grid()





            self.optionsDialog.protocol("WM_DELETE_WINDOW", self.optionsDialogClose)

    def optionsDialogClose(self):
        self.childOpen.set(0)
        self.optionsDialog.destroy()

    def optionsDialogClose2(self,event):
        self.optionsDialogClose()

    def editChannelClose(self):
        if(self.newChannelName.get()!=''):
            self.channel.set(self.newChannelName.get())
            self.newChannelName.set('')
            #attempt to join new channel
        self.childOpen.set(0)
        self.channelEdit.destroy()

    def editChannelClose2(self,event):
        self.editChannelClose()

    def editChannelCloseWM(self):
        self.newChannelName.set('')
        self.editChannelClose()

    def customAutomatedModerator(self):
        self.openOptions()
        #set moderator options to active with caret

    def getOauth(self):
        #get that pass somehow
        pass

    def userValidate(self,username):
        #check to see if entered username is valid twitch username
        pass

    def stackSend(self):
        if(len(self.chatStack)):
            output = self.chatStack.pop(0)
        else:
            output=['']
        return(output)

    def extractChat(self,message):
        Error = 'Error.extractChat x'
##        try:
        if(message[1:4] == "'',"):
            msg = message.split("', '")
            if(len(msg) == 3):
                msg = msg[1].split(' ')[1]
                #message = message.split(',')[2:].strip(' ').strip("]").strip("'")
                if(msg == 'PRIVMSG'):
                    msgID = str(message.split("', '")[1].split('.')[0].split('!')[0])
                    if(msgID == 'jtv'):
                        msgID = 'Server'
                    msgID = msgID + ':'
                    message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    message = self.styleChat(message)
                    return(msgID,message)
                elif(msg == 'JOIN'):
                    msgID = 'Server:'
                    message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                    self.joinUsers(message)
                    return(msgID,(message+' has joined.'))
                elif(msg == 'PART'):
                    msgID = 'Server:'
                    message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                    self.partUsers(message)
                    return(msgID,(message+' has left.'))
                elif(msg in ['001','002','003','004','375','372','376']):
                    msgID = 'Server:'
                    message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    return(msgID,('"'+message+'"'))
                elif(msg == '353'):
                    msgID = 'Server:'
                    #self.userlisterror.clear()
                    self.userlisterror.append(message)
                    self.messagelen.append(len(message))
                    #self.extractUsers(len(message))
                    message =  ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    self.extractUsers(message)
                    return(msgID,("NAMES-"+message))
                elif(msg == '366'):
                    self.userlisterror.clear()
                    message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    msgID = 'Server:'
                    return(msgID,("--"+message+"--"))
                elif(msg == 'MODE'):
                    msgID = 'Server:'
                    message = "".join(message.split("', '")[1][9:]).strip(']').strip("'")
                    return(msgID,message)
                else:
                    msgID = ''
                    #(msgID,message)=
                    self.chatError(msg,msgID,message)
                    return(msgID,(Error +"004: -("+msg+')'+message))
            elif(len(msg) == 2):
                if(len(msg)>=2):
                    if(len(msg[1].split(' '))>=2):
                        msg=msg[1].split(' ')[1]
                        if(msg == 'PART'):
                            msgID = 'Server:'
                            message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                            self.partUsers(message)
                            return(msgID,(message+" has left."))
                        elif(msg == 'JOIN'):
                            msgID = 'Server:'
                            message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                            self.joinUsers(message)
                            return(msgID,(message+" has joined."))
                        elif(msg=='535'):
                            msgID='Server:'
                            self.userlisterror.append(message)
                        elif(msg == 'MODE'):
                            #potentially other options besides +o to account for here someday - not sure
                            msgID = 'Server:'
                            message = "".join(message.split("', '")[1][9:]).strip(']').strip("'")
                            return(msgID,message)
                        elif(msg == 'PRIVMSG'):
                            msgID = message.split("', '")[1].split('.')[0].split('!')[0]
                            msgID = msgID + ':'
                            message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip('"')
                            message = self.styleChat(message)
                            return(msgID,message)
                        else:
                            msgID = ''
                            self.chatError(msg,msgID,message)
                            return(msgID,(Error +"001: -("+msg+')' + message))
                    else:
                        msgID = ''
                        self.chatError('',msgID,message)
                        return(msgID,(Error+"010: -"+message))
                else:
                    msgID = ''
                    self.chatError('',msgID,message)
                    return(msgID,(Error+'011: -'+message))
            elif(len(msg) >= 4):
                #not exactly sure what this one means yet<-DEPRECATED
                msg = msg[1].split(' ')[1]
                if(msg == 'PRIVMSG'):
                    msgID = message.split("', '")[1].split('.')[0].split('!')[0]
                    msgID = msgID + ':'
                    message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    message = self.styleChat(message)
                    return(msgID,message)
                else:
                    msgID = ''
                    self.chatError(msg,msgID,message)
                    return(msgID,(Error +"006: -("+msg+')'+message))
            else:
                msg = msg[1].split(' ')[1]
                msgID = ''
                self.chatError(msg,msgID,message)
                return(msgID,(Error +"005: -("+msg+')'+message))
        elif(message[1:8] == "'PING '"):
            if(message[11:24] == "tmi.twitch.tv"):
                msgID = 'Server:'
                message = 'PING!'
                return(msgID,message)
            else:
                msgID = ''
                self.chatError('',msgID,message)
                return(msgID,(Error +"002: -"+ message))
        else:
            #further contingencies go here someday
            msgID = ''
            if(self.userlisterror):
                self.userlisterror.append(message)
                (fixable,temp) = self.fixUserList(message)
                if(fixable):
                    message = temp
                    return('Server:',temp.strip("[']"))
                else:
                    self.chatError('',msgID,message)
            else:
                self.chatError('',msgID,message)
            return(msgID,(Error +"003: -"+message))
##        except TypeError:
##            return(Error+"007: -"+message)
##        except AttributeError:
##            return(Error+"008: -"+message)
##        except IndexError:
##            return(Error+"009: -"+message)
##        except:
##            return(Error +"000: -"+message)

    def styleChat(self,message):
        message = message.replace("\\'","'")
        message = message.replace("', '",":")
        message = message.replace('", "',":")
        message = message.replace("""', \"""",":")
        message = message.replace("""", '""",":")
        message = message.replace("\\x01ACTION"," <<")
        message = message.replace("\\x01"," >> ")
        return(message)

    def extractUsers(self,message):
        self.using.extend(message.split(' '))
        self.setUsers()

    def joinUsers(self,user):
        try:
            self.using.append(user)
            self.setUsers()
        except:
            pass

    def partUsers(self,user):
        try:
            self.using.remove(user)
            self.setUsers()
        except:
            pass

    def formatUsers(self,users,data):
        #implement tiered user groups in userslist
        pass

    def fixUserList(self,message):
        fixable = False
        while(len(self.userlisterror)>2):
            self.userlisterror.pop(0)
        if(len(self.userlisterror)==2):
            if(self.userlisterror[1].find(',')==-1 and self.userlisterror[0].split("', '")[1].split(' ')[1]=='353'):
                message = self.userlisterror[0].split("', '")[2].strip(']').strip("'").split(' ')
                message = message[len(message)-1]
                try:
                    self.using.remove(message)
                    self.setUsers()
                    
                except:
                    #this should never happen, but need to make note somehow if it does
                    pass
                message = message + self.userlisterror[1].lstrip('[').rstrip(']').strip("'")
                message = "Recovered:NAMES-" + message
                fixable = True
                self.userlisterror.clear()
            else:
                message = self.userlisterror[0][:len(self.userlisterror[0])-2]+self.userlisterror[1][2:]
                tag = message.split("', '")[1].split(' ')[1]
                if(tag=='353'):
                    message = "Recovered:NAMES-" + message
                    fixable = True
                    self.userlisterror.clear()
                else:
                    message=self.userlisterror.pop(0)
                    self.chatError('','',message)
#                pass
        else:
            pass
        return(fixable,message)

    def setUsers(self):
        self.formatUserList()
        self.users.set(" ".join(self.using).strip('[').strip(']').replace(','," "))

    def chatError(self,msg,msgID,message):
        time = self.timeStamp()
#        ####try inserting a space between message fragments if appending fails####
        #check for message fragments in queue
        #try to combine fragments to recover message
        #write to terminal a "recovered message" with original timestamp
        #if process turns out to be stable enough, write message to chat
        if(self.msgfragments):
            if(len(self.msgfragments)==2):
                oldmessage=message
                message = self.msgfragments[1].rstrip("']")+message.lstrip("['")
                #print(message)
                try:
                    tag = message.split("', '")[1].split(' ')[1]
                    #print(tag)
                    if(tag == 'PRIVMSG'):
                        msgID = str(message.split("', '")[1].split('.')[0].split('!')[0])
                        if(msgID == 'jtv'):
                            msgID = 'Server'
                        msgID = msgID + ':'
                        message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                        message = self.styleChat(message)
                        self.recoverMessage(self.msgfragments[0]+msgID+message,1)
                    elif(tag == 'PART'):
                        msgID = 'Server:'
                        message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                        self.partUsers(message)
                        message=message+" has left."
                    elif(tag == 'JOIN'):
                        msgID = 'Server:'
                        message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                        self.joinUsers(message)
                        message = message+" has joined."
                    elif(tag == 'MODE'):
                        msgID = 'Server:'
                        message = "".join(message.split("', '")[1][9:]).strip(']').strip("'")
                    elif(tag == '353'):
                        msgID = 'Server:'
                        message =  ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                        self.extractUsers(message)
                        message = 'NAMES--'+message
                    elif(tag=='366'):
                        msgID = 'Server:'
                        self.userlisterror.clear()
                        message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    elif(tag in ['001','002','003','004','375','372','376']):
                        msgID = 'Server:'
                        message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                    else:
                        #do no printing here. for now:
                        x=10/0#<-inelegant escape?
                    #print to terminal and maybe chat
                    self.recoverMessage(self.msgfragments[0]+msgID+message,0)
                    self.msgfragments.clear()
                except:
                    message=oldmessage
                    message = self.msgfragments[1].rstrip("']")+' '+message.lstrip("['")
                    try:
                        tag = message.split("', '")[1].split(' ')[1]
                        if(tag == 'PRIVMSG'):
                            msgID = str(message.split("', '")[1].split('.')[0].split('!')[0])
                            if(msgID == 'jtv'):
                                msgID = 'Server'
                            msgID = msgID + ':'
                            message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                            message = self.styleChat(message)
                            self.recoverMessage(self.msgfragments[0]+msgID+message,1)
                        elif(tag == 'PART'):
                            msgID = 'Server:'
                            message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                            self.partUsers(message)
                            message=message+" has left."
                        elif(tag == 'JOIN'):
                            msgID = 'Server:'
                            message = message.split(',')[1].strip(' ').strip("'").strip(' ').split('.')[0].split('@')[0].split('!')[0]
                            self.joinUsers(message)
                            message = message+" has joined."
                        elif(tag == 'MODE'):
                            msgID = 'Server:'
                            message = "".join(message.split("', '")[1][9:]).strip(']').strip("'")
                        elif(tag == '353'):
                            msgID = 'Server:'
                            message =  ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                            self.extractUsers(message)
                            message = 'NAMES--'+message
                        elif(tag=='366'):
                            msgID = 'Server:'
                            self.userlisterror.clear()
                            message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                        elif(tag in ['001','002','003','004','375','372','376']):
                            msgID = 'Server:'
                            message = ",".join(message.split(',')[2:]).strip(' ').strip("]").strip("'")
                        else:
                            #do no printing here. for now:
                            x=10/0#<-inelegant escape?
                        #print to terminal and maybe chat
                        self.recoverMessage(self.msgfragments[0]+msgID+message,0)
                        self.msgfragments.clear()
                    except:
                    #do something clever here
                        pass
            else:
                if(len(message)>=6):
                    if(message[0:5]=="['', "):
                        self.msgfragments.append(time)
                        self.msgfragments.append(message)
                    elif(message[0:10]=="['PING ', "):
                        #eventually handle broken pings
                        pass
                    else:
                        #try to handle this as well
                        self.msgfragments.append(time)
                        self.msgfragments.append(message)
                else:
                    #write this error to log
                    self.msgfragments.append(time)
                    self.msgfragments.append(message)

        else:
            if(len(message)>=6):
                if(message[0:5]=="['', "):
                    self.msgfragments.append(time)
                    self.msgfragments.append(message)
                elif(message[0:10]=="['PING ', "):
                    #eventually handle broken pings
                    pass
                else:
                    #try to handle whatever this is
                    #this one is also probably not recoverable
                    pass
            else:
               #write this error to log:-probably not recoverable
               pass

    def recoverMessage(self,message,chat):
        if(chat==0):
            self.terminalWrite('Recovered:',message)
        if(chat==1):
            #if this becomes reliable enough, remove the 'Recovered:' prefix from chatWrite
            self.chatWrite('Recovered:',message)

    def runTasks(self):
        #run maintenance tasks and utilites
        #perhaps implement priority tiers here?
        self.checkUserMultiplicity()
        

    def checkUserMultiplicity(self):
        #check how many times each user appears in self.using; update self.users
        #make note in log of occurance
        #temporarily print out names that have multiplicities
#        print('Coming soon...')
        for _user in self.using:
            while(True):
                try:
                    index=self.using.index(_user,self.using.index(_user)+1)
                    print(self.using.pop(index))

                except ValueError:
                    break
                except:
                    #unexpected error needs to be logged
                    break

        self.setUsers()
