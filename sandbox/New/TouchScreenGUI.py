'''
Created on Jan 25, 2016

@author: stacypickens
'''
from Tkinter import *
from production.Supervisor import Supervisor
from multiprocessing import Process

#create a title for the window
#running = False

root = Tk()
root.wm_title("AU Photo Upload")

#place an image in the window
img = PhotoImage(file='tiger.gif')
root.tk.call('wm', 'iconphoto', root._w, img)

#functions defined to run scripts

def UploadPhotos(event):
    print("Test for script to upload photos")
    
    running = False
    
    if running is False:
        supervisor = Supervisor()
        process = Process(target=supervisor.run())
        running = True
        process.start()
        process.join()
        
    if running is True:
        process.terminate()  
        running = False

def FileExplorer(event):
    print("Test for script to file explorer")

def Settings(event):
    print("Test for script to settings")
  
#header label at the top of window  
label = Label(root, text="AU Photo Upload", bg="orange", fg="white", font = "Verdana 15")
label.pack(fill=X)

topFrame = Frame(root)
topFrame.pack()

#information for button1
button1 = Button(topFrame, text="Upload Photos", width=12, height=12, bg="orange", fg="white", font = "Verdana 12")
button1.bind("<Button-1>", UploadPhotos)

#information for button2
button2 = Button(topFrame, text="File Explorer", width=12, height=12, bg="orange", fg="white", font = "Verdana 12")
button2.bind("<Button-2>", FileExplorer)

#information for button3
button3 = Button(topFrame, text="Settings", width=12, height=12, bg="orange", fg="white", font = "Verdana 12")
button3.bind("<Button-3>", Settings)

#pack all information for the buttons 
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)


root.mainloop()