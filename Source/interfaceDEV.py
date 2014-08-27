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
        self.createMainWindow()
        chatInput = tk.StringVar()

    def launch(self):
        self.splash()
        self.allocateVars()
        #load control values from config

        #run startup tasks eventually
        #meanwhile:
        time.sleep(3)

        self.loadingSplash.destroy()

    def splash(self):
        self.loadingSplash = tk.Tk()
        self.logo = tk.PhotoImage(file='sirbot.gif')
        self.loading = ttk.Label(self.loadingSplash,image=self.logo)
        self.loadingSplash.overrideredirect(True)
        self.loading.pack()

        top = self.loading.winfo_toplevel()
        self.h = self.loading.winfo_screenheight()
        self.w = self.loading.winfo_screenwidth()
        self.hmm = self.loading.winfo_screenmmheight()
        self.wmm = self.loading.winfo_screenmmwidth()

        self.loadingSplash.wm_attributes('-alpha',0.75)
        self.loadingSplash.update_idletasks()
        self.loadingSplash.geometry()
        self.loadingSplash.geometry('262x112+'+str(int(self.w/2)-131*1)+
                                    '+'+str(int(self.h/2)-56*1))
        self.loadingSplash.update_idletasks()
        self.loadingSplash.update()

    def allocateVars(self):
        #informative
        self.botName = 'SirBot'
        self.botVersion = '0.0.0'

        #queues
        self.chatStack = []
        self.messagelen = []
        self.msgfragments = []
        self.userlisterror = []

        #tk control variables
        self.editConfig = tk.IntVar()
        self.autoMod = tk.IntVar()
        self.childOpen = tk.IntVar()
        self.newChannelName = tk.StringVar()
        self.ownerUpdate = tk.StringVar()
        self.chatInput = tk.StringVar()
        self.onTop = tk.IntVar()

        self.editConfig.set(0)
        self.autoMod.set(1)
        self.childOpen.set(0)
        self.newChannelName.set('')
        self.ownerUpdate.set('')
        self.chatInput.set('')
        self.onTop.set(0)


        #tk user variables
        self.channel = tk.StringVar()
        self.owner = tk.StringVar()
        self.password = tk.StringVar()
        self.users = tk.StringVar()

        #master user list
        self.using = []
        

    def createMainWindow(self):
        self.MainWindow = tk.Tk()
        self.MainWindow.title(self.botName+' v'+self.botVersion)
        self.createTerminalSIMPLE()

    def createTerminalSIMPLE(self):
        self.terminalFrame = ttk.Frame(self.MainWindow)
        self.createTerminalHistory()
        self.createTerminalInput()

    def createTerminalInput(self):
        self.terminalInput = ttk.Entry(self.terminalFrame,cursor='xterm',
                                       textvariable=self.chatInput)
        self.terminalEnter = ttk.Button(self.terminalFrame,text='Enter')

        self.terminalInput.grid(in_=self.terminalFrame,row=1,column=0,sticky='EW',
                                columnspan=11)
        self.terminalEnter.grid(in_=self.terminalFrame,row=1,column=11,sticky='EW',
                                columnspan=2)
        

    def createTerminalHistory(self):
        #self.terminalFrame = ttk.Frame(self.MainWindow)
        self.terminalScroll = ttk.Scrollbar(self.terminalFrame,orient=tk.VERTICAL)
        self.terminalHistory = tk.Text(self.terminalFrame,bg='white',fg='black',
                                   height=32,width=75,takefocus=0,
                                   state='disabled',
                                   yscrollcommand=self.terminalScroll.set)
        self.terminalScroll['command'] = self.terminalHistory.yview
        
        

        self.terminalFrame.grid(in_=self.MainWindow,row=1,column=0,sticky='NSEW')
        self.terminalHistory.grid(in_=self.terminalFrame,row=0,column=0,sticky='NSEW',
                                  columnspan=12)
        self.terminalScroll.grid(in_=self.terminalFrame,row=0,column=12,sticky='NSW')
        
        

    def createTEMP(self):
        self.Main = ttk.Frame(self.MainWindow)
        self.button = ttk.Button(self.Main,text='Button')

        self.Main.grid()
        self.button.grid(sticky='NSEW')
        

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
