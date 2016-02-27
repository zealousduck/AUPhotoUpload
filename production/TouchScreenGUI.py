'''
Created on Jan 25, 2016

@author: stacypickens
'''
import os
from Tkinter import *
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
        root = Tk()
        root.wm_title("AU Photo Upload")
        #img = PhotoImage(file='tiger.gif')
        #root.tk.call('wm', 'iconphoto', root._w, img)
        label = Label(root, text="AU Photo Upload", bg="orange", fg="white", font = "Verdana 15")
        label.pack(fill=X)
        
        topFrame = Frame(root)
        topFrame.pack()
        
        #information for Upload Photos (continuous)
        button1 = Button(topFrame, text="Upload Photos", width=12, height=12, bg="orange", fg="white", font = "Verdana 12")
        button1.bind("<Button-1>", self.ContinuousUploadToggle)
        
        #information for button2
        button2 = Button(topFrame, text="File Explorer", width=12, height=12, bg="orange", fg="white", font = "Verdana 12")
        button2.bind("<Button-1>", self.FileExplorer)
        
        #information for button3
        button3 = Button(topFrame, text="Settings", width=12, height=12, bg="orange", fg="white", font = "Verdana 12")
        button3.bind("<Button-1>", self.Settings)
        
        #pack all information for the buttons 
        button1.pack(side=LEFT)
        button2.pack(side=LEFT)
        button3.pack(side=LEFT)
        return root

    def ContinuousUploadToggle(self, event):
         
        if self.toggle is False:
            print("Turning on photo upload...")    
            #process = Process(target= self.startSupervisor)
            #process.start()
            self.toggle = True
            self.queue.put("ContinuousUploadCreate")
            #self.root = self.TkSetup()
            #self.run()
            # process.join()     
        else: 
            print("Turning off photo upload...")
            self.toggle = False
            self.queue.put("ContinuousUploadKill")
    
    def FileExplorer(self, event):
        print("Test for script to file explorer")
        self.queue.put("FileExplorer")
    
    def Settings(self, event):
        print("Test for script to settings")
        self.queue.put("Settings")
        
    def startSupervisor(self):
        svisor = Supervisor.Supervisor()
        svisor.run()
        
if __name__ == '__main__':
    blah = Queue()
    FrontEnd().run(blah)
  
