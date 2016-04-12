'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
import PhotoUploadUtility as Utility
from multiprocessing import Queue


class FrontEnd(object):
    messageDict = {Utility.QMSG_SCAN: "Scanning\n For New\n Images...",
                    Utility.QMSG_SCAN_DONE: "Scan\n Complete.",
                    Utility.QMSG_UPLOAD: "Uploading\n In\n Progress...",
                    Utility.QMSG_UPLOAD_DONE: "Uploading\n Complete.",
                    Utility.QMSG_HANDLE_NONE: "No new\n images\n found.",
                    Utility.QMSG_IDLE: "Idle"};
    def __init__(self, taskQueue, statusQueue):
        self.toggle = False     # Variable for constant-upload mode
        self.queue = taskQueue
        self.gearState = 0
        self.myGear = None
        self.myImages = {
                         Utility.QMSG_SCAN: "ima1",
                         Utility.QMSG_SCAN_DONE: "ima2",
                         Utility.QMSG_UPLOAD: "ima3",
                         Utility.QMSG_UPLOAD_DONE: "ima4",
                         Utility.QMSG_HANDLE_NONE: "ima5",
                         Utility.QMSG_IDLE: "ima6"
                         }
        self.statusQueue = statusQueue
        self.currentStatus = Utility.QMSG_IDLE
        self.currentPhoto = None
        self.root = self.TkSetup()
        
    
    def run(self):
        print "TouchScreenGUI, checking in! pid:", os.getpid()
        self.root.after(1000, self.getMsgTask)
        self.root.after(20, self.DriveGear)
        self.root.mainloop()
    
    def TkSetup(self):
        from Tkinter import *
        root = Tk()
        root.wm_title("Photo Upload")
        #img = PhotoImage(file='tiger.gif')
        #root.tk.call('wm', 'iconphoto', root._w, img)
        label = Label(root, text="Photo Upload", bg="orange", fg="white", font = "Verdana 15")
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
        self.button5 = Button(root, text="", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button6 = Label(topFrame, text="", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        #pack all information for the buttons 
        self.currentPhoto = PhotoImage(file = "ima6.gif")
        self.myGear = PhotoImage(file = "gears.gif")
        self.button1.pack(side=LEFT)
        self.button2.pack(side=LEFT)
        self.button3.pack(side=LEFT)
        self.button4.pack(side=LEFT)
        self.button5.pack(side=BOTTOM)
        self.button6.pack(side=LEFT)
        return root
    
    def DisplayCurrentStatus(self, pendingStatus):
        from Tkinter import PhotoImage, BOTTOM
        displayText = ""
        if pendingStatus in FrontEnd.messageDict:
            displayText = FrontEnd.messageDict[pendingStatus]
        else:
            displayText = "Error: \nUnknown \nStatus."
        self.currentStatus = pendingStatus
        self.button4["text"] = displayText
        self.currentPhoto = PhotoImage(file = self.myImages[pendingStatus] + ".gif")
        self.button5.config(image= self.currentPhoto, width="500", height="64")
        self.button5.pack(side=BOTTOM)
        
    def DriveGear(self):
        from Tkinter import PhotoImage, BOTTOM, TOP, LEFT
        self.myGear = PhotoImage(file = "gears.gif", format=str("gif -index " + str(self.gearState)))
        self.button6.config(image= self.myGear, width="120", height="120")
        self.button6.pack(side=LEFT)
        self.gearState += 1
        if self.gearState > 19:
            self.gearState = 0
        self.root.after(20, self.DriveGear) 
    
    def StartUpload(self, event):
        self.queue.put(Utility.QMSG_START)
        
    def getMsgTask(self):
        statusMessage = ""
        if(self.statusQueue.empty()):
            statusMessage = self.currentStatus
        else:
            statusMessage = self.statusQueue.get() 
        self.DisplayCurrentStatus(statusMessage)
 
        self.root.after(Utility.POLL_TIME*1000, self.getMsgTask) # scheduled in ms
    
    def FileExplorer(self, event):
        print("Test for script to file explorer")
        self.queue.put(Utility.QMSG_FILE_EXPLORER)
    
    def Settings(self, event):
        print("Test for script to settings")
        self.queue.put(Utility.QMSG_SETTINGS)
        
