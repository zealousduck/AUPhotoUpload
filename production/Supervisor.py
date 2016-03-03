'''
Created on Feb 3, 2016

Supervisor.py is the parent class and entry point for the PhotoUpload
    application. It creates the child classes that perform the work.
    Direct child processes: Reader, Handler, FrontEnd
'''
import PhotoUploadConstants as constants
import PhotoUploadUtility as utility
import Reader
import Handler
import os
import time
import TouchScreenGUI as tsgui
from multiprocessing import Process, Queue
import subprocess

class Supervisor(object):

    def __init__(self):
        self.guiQueue = Queue()
        self.handlerQueue = Queue()
        self.readerQueue = Queue()
    
    def startReader(self):
        self.readerQueue.put("run")
        reader = Reader.Reader(self.readerQueue)
        reader.run()
    
    def startHandler(self):
        self.handlerQueue.put("run")
        handler = Handler.Handler(self.handlerQueue)
        handler.run()
        
    def startGUI(self):
        myGui = tsgui.FrontEnd(self.guiQueue)
        myGui.run()
    
    def run(self):
        print "Supervisor, checking in! pid:", os.getpid()
        # If image directory does not exist yet, create it!
        config = utility.getProjectConfig()
        imgdir = config.get('directories','imagedirectory')
        if not os.path.isdir(imgdir):
            subprocess.call(['mkdir', imgdir])  # os.mkdir might also work
            
        guiProcess = Process(target = self.startGUI)
        guiProcess.start()
        handlerProcess = None
        readerProcess = None
        while True:
            if not self.guiQueue.empty():
                job = self.guiQueue.get()
                if job == "ContinuousUploadCreate":
                    handlerProcess = Process(target = self.startHandler)
                    handlerProcess.start()
                    # READER PROCESS DISABLED FOR CYCLE 1 - REDESIGN PENDING PER WADE'S COMMENTS
                    #readerProcess = Process(target = self.startReader)
                    #readerProcess.start()
                    
                elif job == "ContinuousUploadKill":
                    print "Killing Processes ... (they may still check in a few more times, this is normal)"
                    self.handlerQueue.get() #Tells the Handler process to finish.
                    self.readerQueue.get() #Tells the Reader process to finish.
                    handlerProcess.join() #Wait for the Handler process to finish.
                    #readerProcess.join() #Wait the Reader process to finish.
                    print "Done killing processes."
                elif job == "Settings":
                    print "Supervisor handles Settings job here if needed"
                else:
                    raise Exception('Supervisor.run:  unexpected object in queue')
            time.sleep(constants.POLL_TIME)
    
if __name__ == '__main__':
    Supervisor().run()
    
        
