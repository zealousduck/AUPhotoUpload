'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
import PhotoUploadUtility as Utility
from multiprocessing import Queue


class FrontEnd(object):
    
    def __init__(self, taskQueue, statusQueue):
        self.toggle = False     # Variable for constant-upload mode
        self.queue = taskQueue
        self.statusQueue = statusQueue
        self.currentStatus = "Idle"
        self.root = self.TkSetup()
        
    
    def run(self):
        print "TouchScreenGUI, checking in! pid:", os.getpid()
        self.root.after(1000, self.getMsgTask)
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
        self.button2 = Button(topFrame, text="File Explorer", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button2.bind("<Button-1>", self.FileExplorer)
        
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
        if(pendingStatus == Utility.QMSG_SCAN):
            displayText = "Scanning\n For New\n Images..."
        elif(pendingStatus == Utility.QMSG_SCAN_DONE):
            displayText = "Scan\n Complete."
        elif(pendingStatus == Utility.QMSG_UPLOAD):
            displayText = "Uploading\n In\n Progress..."
        elif(pendingStatus == Utility.QMSG_UPLOAD_DONE):
            displayText = "Uploading\n Complete."
        elif(pendingStatus == Utility.QMSG_HANDLE_NONE):
            displayText = "No new\n images\n found."
        elif(pendingStatus == "Idle"):
            displayText = "Idle"
        elif(pendingStatus == "all your base."):
            displayText = "all your base."
        else:
            displayText = "Error: \nUnknown \nStatus."
            
        self.currentStatus = pendingStatus
        self.button4["text"] = displayText
    
    def StartUpload(self, event):
        self.queue.put(Utility.QMSG_START)
        
    def getMsgTask(self):
        
        # read message queue
        #     is message queue empty?
        #     queue.empty() returns true or false
        #     if yes, do nothing
        #     if no, check message
        statusMessage = ""
        if(self.statusQueue.empty()):
            statusMessage = self.currentStatus
        else:
            statusMessage = self.statusQueue.get() 
        self.DisplayCurrentStatus(statusMessage)
        # check what the message is
        #    e.g. MSG=working, display a loading icon
        #    e.g. MSG=done, display a checkmark
        
        # reschedule this task after working
        self.root.after(1000, self.getMsgTask) 
    
    def FileExplorer(self, event):
        print("Test for script to file explorer")
        self.queue.put(Utility.QMSG_FILE_EXPLORER)
    
    def Settings(self, event):
        print("Test for script to settings")
        self.queue.put(Utility.QMSG_SETTINGS)
        
