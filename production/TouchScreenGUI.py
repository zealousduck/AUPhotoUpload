'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
from multiprocessing import Process, Queue


class FrontEnd(object):
    
    def __init__(self, sQueue):
        self.toggle = False     # Variable for constant-upload mode 
        self.root = self.TkSetup() 
        self.queue = sQueue
    
    def run(self):
        print "TouchScreenGUI, checking in! pid:", os.getpid()
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
        self.button1 = Button(topFrame, text="Upload Photos: \nOFF", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button1.bind("<Button-1>", self.ContinuousUploadToggle)
        
        #information for button2
        self.button2 = Button(topFrame, text="File Explorer", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button2.bind("<Button-1>", self.FileExplorer)
        
        #information for button3
        self.button3 = Button(topFrame, text="Settings", width=14, height=12, bg="orange", fg="white", font = "Verdana 12")
        self.button3.bind("<Button-1>", self.Settings)
        
        #pack all information for the buttons 
        self.button1.pack(side=LEFT)
        self.button2.pack(side=LEFT)
        self.button3.pack(side=LEFT)
        return root

    def ContinuousUploadToggle(self, event):
        if self.toggle is False:
            print("Turning on photo upload...")    
            self.toggle = True
            self.queue.put("ContinuousUploadCreate")
            self.button1.config(text="Upload Photos: \nON")
        else: 
            print("Turning off photo upload...")
            self.toggle = False
            self.queue.put("ContinuousUploadKill")
            self.button1.config(text="Upload Photos: \nOFF")
    
    def FileExplorer(self, event):
        print("Test for script to file explorer")
        self.queue.put("FileExplorer")
    
    def Settings(self, event):
        print("Test for script to settings")
        self.queue.put("Settings")
        
