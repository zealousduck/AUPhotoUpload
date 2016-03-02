'''
Created on Jan 25, 2016

@author: stacypickens
'''
from Tkinter import *
from production.Supervisor import Supervisor
from multiprocessing import Process

class FrontEnd(object):
    
    def __init__(self):
        self.toggle = False     # Variable for constant-upload mode 
        self.root = self.TkSetup() 
    
    def run(self):
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
        button1on = Button(topFrame, text="Upload Photos On", width=12, height=16, bg="orange", fg="white", font = "Verdana 12")
        button1on.bind("<Button-1>", self.ContinuousUploadToggle)
        
        #information for button2
        button2 = Button(topFrame, text="File Explorer", width=12, height=16, bg="orange", fg="white", font = "Verdana 12")
        button2.bind("<Button-2>", self.FileExplorer)
        
        #information for button3
        button3 = Button(topFrame, text="Settings", width=12, height=16, bg="orange", fg="white", font = "Verdana 12")
        button3.bind("<Button-3>", self.Settings)
        
        #pack all information for the buttons 
        button1on.pack(side=LEFT)
        button2.pack(side=LEFT)
        button3.pack(side=LEFT)
        return root

    def ContinuousUploadToggle(self, event):
        print("Test for script to upload photos")       
        if self.toggle is False:
            supervisor = Supervisor()
            process = Process(target=supervisor.run())
            self.toggle = True
            process.start()
            # process.join()     
        if self.toggle is True:
            process.terminate()  
            self.toggle = False
    
            
    def FileExplorer(self, event):
        print("Test for script to file explorer")
    
    def Settings(self, event):
        print("Test for script to settings")
        
if __name__ == '__main__':
    FrontEnd().run()
  
