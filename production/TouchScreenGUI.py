'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
import PhotoUploadUtility as Utility
from multiprocessing import Queue


class FrontEnd(object):
    messageDict = { Utility.QMSG_SCAN: ("Scanning and\nDownloading New\nImages\n(This could\ntake a while...)", 4),
                    Utility.QMSG_SCAN_DONE: ("Scan\nComplete.",  4),
                    Utility.QMSG_SCAN_FAIL: ("Scan\nFailed.",  4),
                    Utility.QMSG_UPLOAD: ("Uploading\nIn\nProgress...", 4),
                    Utility.QMSG_UPLOAD_DONE: ("Uploading\nComplete.", 4),
                    Utility.QMSG_HANDLE_NONE: ("No new\nimages\nfound.", 4),
                    Utility.QMSG_IDLE: ("Idle", 4),
                    Utility.QMSG_INTERNET_NO: ("No\nInternet\nConnection", 2),
                    Utility.QMSG_INTERNET_YES: ("Internet\nConnection\nAvailable", 2)};
    errorButton = 4
    errorStatus = "Error:\nUnknown\nStatus."
    
    def __init__(self, taskQueue, statusQueue):
        self.toggle = False     # Variable for constant-upload mode
        self.queue = taskQueue
        self.statusQueue = statusQueue
        self.currentStatus = Utility.QMSG_IDLE
        self.root = self.TkSetup()   
    
    def run(self):
        print "TouchScreenGUI, checking in! pid:", os.getpid()
        self.root.after(Utility.POLL_TIME*1000, self.getMsgTask) # scheduled in milliseconds
        self.root.mainloop()
    
    def TkSetup(self):
        from Tkinter import *
        root = Tk()
        root.wm_title("AU Photo Upload")
        #img = PhotoImage(file='tiger.gif')
        #root.tk.call('wm', 'iconphoto', root._w, img)
        label = Label(root, text="AU Photo Upload", bg="orange", fg="white", font = "Verdana 15")
        label.pack(fill=X)
        
        topFrame = Frame(root)
        topFrame.pack()
        
        #information for Upload Photos (continuous)
        self.button1 = Button(topFrame, text="Start Upload", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button1.bind("<Button-1>", self.StartUpload)
        
        #information for button2
        self.button2 = Button(topFrame, text="Internet\nConnection?", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        #self.button2 = Button(topFrame, text="File Explorer", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        #self.button2.bind("<Button-1>", self.FileExplorer)
        
        #information for button3
        self.button3 = Button(topFrame, text="Settings", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button3.bind("<Button-1>", self.Settings)
        
        self.button4 = Button(topFrame, text=self.currentStatus, width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
    
        #pack all information for the buttons 
        self.button1.pack(side=LEFT)
        self.button2.pack(side=LEFT)
        self.button3.pack(side=LEFT)
        self.button4.pack(side=LEFT)
        return root
    
    def DisplayCurrentStatus(self, pendingStatus):
        displayText = ""
        whichButton = 0
        if pendingStatus in FrontEnd.messageDict:
            displayText, whichButton = FrontEnd.messageDict[pendingStatus]
            #whichButton = FrontEnd.buttonDict[pendingStatus]
        else:
            displayText = FrontEnd.errorStatus
            whichButton = FrontEnd.errorButton
        if(pendingStatus == Utility.QMSG_SCAN_DONE):
            self.button1["text"] = "Start Upload"
        elif(pendingStatus == Utility.QMSG_SCAN_FAIL):
            self.button1["text"] = "Scan\nCamera"
        self.currentStatus = pendingStatus
        if whichButton == 4:
            self.button4["text"] = displayText
        elif whichButton == 2:
            self.button2["text"] = displayText
        else:
            self.button2["text"] = "error"
            self.button4["text"] = "error"
    
    def StartUpload(self, event):
        self.queue.put(Utility.QMSG_START)
        
    def getMsgTask(self):
        statusMessage = ""
        if not (self.statusQueue.empty()):
            statusMessage = self.statusQueue.get() 
            self.DisplayCurrentStatus(statusMessage)
 
        self.root.after(Utility.POLL_TIME*1000, self.getMsgTask) # scheduled in ms
    
    def FileExplorer(self, event):
        print("Test for script to file explorer")
        self.queue.put(Utility.QMSG_FILE_EXPLORER)
    
    def Settings(self, event):
        print("Test for script to settings")
        self.queue.put(Utility.QMSG_SETTINGS)
        
