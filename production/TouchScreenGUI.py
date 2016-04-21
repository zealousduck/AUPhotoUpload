'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
import PhotoUploadUtility as Utility
from multiprocessing import Queue
from Tkconstants import RIGHT


class FrontEnd(object):
    
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
        root.geometry("320x240")
        root.overrideredirect(1)
        #root.wm_title("AU Photo Upload")
        #img = PhotoImage(file='tiger.gif')
        #root.tk.call('wm', 'iconphoto', root._w, img)
#         label = Label(root, text="AU Photo Upload", bg="orange", fg="white", font = "Verdana 15")
#         label.pack(fill=X)
        
        topFrame = Frame(root)
        topFrame.pack()
        

        
        #information for Upload Photos (continuous)
        self.button1 = Button(topFrame, text="Start Upload", width=9, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button1.bind("<Button-1>", self.StartUpload)
        
        #information for button2
        self.button2 = Button(topFrame, text="Internet\nConnection?", width=6, height=6, bg="orange", fg="white", font = "Verdana 12")
        #self.button2 = Button(topFrame, text="File Explorer", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        #self.button2.bind("<Button-1>", self.FileExplorer)
        
        #information for button3
        self.button3 = Button(topFrame, text="Restart", width=9, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button3.bind("<Button-1>", self.Settings)
        
        self.button4 = Button(topFrame, text=self.currentStatus, width=6, height=6, bg="orange", fg="white", font = "Verdana 12")
    
        #pack all information for the buttons 
        self.button1.pack(side=LEFT, anchor=W, fill=Y)
        self.button3.pack(side=RIGHT, anchor=E, fill=Y)
        self.button2.pack(side=TOP, anchor=NW, fill=Y)
        self.button4.pack(side=BOTTOM, anchor=SW, fill=Y)
        return root
    
    def DisplayCurrentStatus(self, pendingStatus):
        # NEEDS REFACTORING INTO SOME DICTIONARY SHIT
        displayText = ""
        whichButton = 0
        if(pendingStatus == Utility.QMSG_SCAN):
            displayText = "Scanning and\nDownloading New\nImages\n(This could\ntake a while...)"
            whichButton = 4
        elif(pendingStatus == Utility.QMSG_SCAN_DONE):
            displayText = "Scan\nComplete."
            whichButton = 4
            self.button1["text"] = "Start Upload"
        elif(pendingStatus == Utility.QMSG_SCAN_FAIL):
            displayText = "Scan\nFailed."
            whichButton = 4
            self.button1["text"] = "Scan\nCamera"
        elif(pendingStatus == Utility.QMSG_UPLOAD):
            displayText = "Uploading\nIn\nProgress..."
            whichButton = 4
        elif(pendingStatus == Utility.QMSG_UPLOAD_DONE):
            displayText = "Uploading\nComplete."
            whichButton = 4
        elif(pendingStatus == Utility.QMSG_HANDLE_NONE):
            displayText = "No new\nimages\nfound."
            whichButton = 4
        elif(pendingStatus == Utility.QMSG_IDLE):
            displayText = "Idle"
            whichButton = 4
        elif(pendingStatus == Utility.QMSG_INTERNET_NO):
            displayText = "No\nInternet\nConnection"
            whichButton = 2
        elif(pendingStatus == Utility.QMSG_INTERNET_YES):
            displayText = "Internet\nConnection\nAvailable"
            whichButton = 2
        else:
            displayText = "Error: \nUnknown \nStatus."
            
        self.currentStatus = pendingStatus
        if whichButton == 4:
            self.button4["text"] = displayText
        elif whichButton == 2:
            self.button2["text"] = displayText
    
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
        
