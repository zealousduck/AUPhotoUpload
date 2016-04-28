'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
import PhotoUploadUtility as Utility
from multiprocessing import Queue
from Tkconstants import RIGHT
from Tkinter import *


class FrontEnd(object):
    __WORKFLOW_BUTTON = 4
    __INTERNET_BUTTON = 2

    statusDict = {  Utility.QMSG_SCAN: ("Scanning\nand\nGetting\nNew\nImages",__WORKFLOW_BUTTON),
                    Utility.QMSG_SCAN_DONE: ("Scan\nComplete",__WORKFLOW_BUTTON),
                    Utility.QMSG_SCAN_FAIL: ("Scan\nFailed",__WORKFLOW_BUTTON),
                    Utility.QMSG_UPLOAD: ("Upload\nin\nProgress",__WORKFLOW_BUTTON),
                    Utility.QMSG_UPLOAD_DONE: ("Upload\nComplete",__WORKFLOW_BUTTON),
                    Utility.QMSG_UPLOAD_USER_FAIL: ("Upload\nFailed:\nCan't\nReach\nDropbox",__WORKFLOW_BUTTON),
                    Utility.QMSG_UPLOAD_IMAGE_FAIL: ("Upload\nComplete*\nSome Images\nFailed",__WORKFLOW_BUTTON),
                    Utility.QMSG_HANDLE_NONE: ("No New\nImages\nFound",__WORKFLOW_BUTTON),
                    Utility.QMSG_IDLE: ("Idle",__WORKFLOW_BUTTON),
                    Utility.QMSG_SLEEP: ("Device\nAsleep",__WORKFLOW_BUTTON),
                    Utility.QMSG_DELAYED: ("Upload To\nContinue\nWhen\nInternet\nResumes",__WORKFLOW_BUTTON),
                    Utility.QMSG_INTERNET_NO: ("Internet\nNot\nConnected",__INTERNET_BUTTON),
                    Utility.QMSG_INTERNET_YES: ("Internet\nConnected",__INTERNET_BUTTON)};
                    
#     buttonDict = {  Utility.QMSG_SCAN:         4,
#                     Utility.QMSG_SCAN_DONE:    4,
#                     Utility.QMSG_SCAN_FAIL:    4,
#                     Utility.QMSG_UPLOAD:       4,
#                     Utility.QMSG_UPLOAD_DONE:  4,
#                     Utility.QMSG_HANDLE_NONE:  4,
#                     Utility.QMSG_IDLE:         4,
#                     Utility.QMSG_INTERNET_NO:  2,
#                     Utility.QMSG_INTERNET_YES: 2};

    errorButton = __WORKFLOW_BUTTON
    errorStatus = "Error:\nUnknown\nStatus."
    
    def __init__(self, taskQueue, statusQueue):
        self.toggle = False     # Variable for constant-upload mode
        self.queue = taskQueue
        self.statusQueue = statusQueue
        self.currentStatus = Utility.QMSG_IDLE
        self.root = self.TkSetup()   
    
    
    def displayCurrentStatus(self, pendingStatus):
        displayText = ""
        whichButton = 0
        if pendingStatus in FrontEnd.statusDict:
            displayText, whichButton = FrontEnd.statusDict[pendingStatus]
            #whichButton = FrontEnd.buttonDict[pendingStatus]
        else:
            print 'not in dict:', pendingStatus
            displayText = FrontEnd.errorStatus
            whichButton = FrontEnd.errorButton
        if(pendingStatus == Utility.QMSG_SCAN_DONE):
            self.startButton["text"] = "Start\nUpload"
        elif(pendingStatus == Utility.QMSG_SCAN_FAIL):
            self.startButton["text"] = "Scan\nCamera"
        self.currentStatus = pendingStatus
        if whichButton == 4:
            self.statusLabel["text"] = displayText
        elif whichButton == 2:
            self.internetLabel["text"] = displayText
    
    def startUpload(self, event):
        self.queue.put(Utility.QMSG_START)
        
    def getMsgTask(self):
        statusMessage = ""
        if not (self.statusQueue.empty()):
            statusMessage = self.statusQueue.get() 
            self.displayCurrentStatus(statusMessage)
 
        self.root.after(Utility.POLL_TIME*1000, self.getMsgTask) # scheduled in ms
    
    def fileExplorer(self, event):
        print("Test for script to file explorer")
        self.queue.put(Utility.QMSG_FILE_EXPLORER)
    
    def resetFunc(self, event):
        print("Test for script to reset")
        self.queue.put(Utility.QMSG_SETTINGS)
        os.system("killall python")
        
    def powerOffFunc(self, event):
        print("Test confirm")
        self.queue.put(Utility.QMSG_SETTINGS)
        os.system("poweroff") 
        #os.system("sudo shutdown -h now")         
    
    def TkSetup(self):
        #from Tkinter import *
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
        self.startButton = Button(topFrame, text="Start\nUpload", width=8, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.startButton.bind("<Button-1>", self.startUpload)
        
        #information for button2
        self.internetLabel = Label(topFrame, text="Checking\nFor\nInternet", width=8, height=6, bg="orange", fg="white", font = "Verdana 12")
        #self.button2 = Button(topFrame, text="File Explorer", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        #self.button2.bind("<Button-1>", self.FileExplorer)
        
        #information for button3
        self.resetButtion = Button(topFrame, text="Restart", width=8, height=6, bg="orange", fg="white", font = "Verdana 12")
        self.resetButtion.bind("<Button-1>", self.resetFunc)
        
        self.statusLabel = Label(topFrame, text="Starting\nUp", width=8, height=6, bg="orange", fg="white", font = "Verdana 12")
        
        self.powerOffButton = Button(topFrame, text="Power\nOff", width=8, height=6, bg="orange", fg="white", font="Verdana 12")
        self.powerOffButton.bind("<Button-1>", self.powerOffFunc)
        
        #pack all information for the buttons 
#         self.startButton.pack(side=LEFT, anchor=W)
#         self.resetButtion.pack(side=RIGHT, anchor=E)
#         self.internetLabel.pack(side=TOP, anchor=NW)
#         self.statusLabel.pack(side=BOTTOM, anchor=SW)
#         return root
    
        
        self.startButton.grid(column=0, rowspan=2)
        self.internetLabel.grid(row=0, column=1)
        self.statusLabel.grid(row=1, column=1)
        self.powerOffButton.grid(row=0, column=2)
        self.resetButtion.grid(row=1, column=2)
        return root

    def run(self):
        print "TouchScreenGUI, checking in! pid:", os.getpid()
        self.root.after(Utility.POLL_TIME*1000, self.getMsgTask) # scheduled in milliseconds
        self.root.mainloop()
        
