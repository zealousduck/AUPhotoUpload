'''
Created on Feb 3, 2016

Supervisor.py is the parent class and entry point for the PhotoUpload
    application. It creates the child classes that perform the work.
    Direct child processes: Reader, Handler
'''
import PhotoUploadUtility as Utility
import Reader
import Handler
import os
import errno
import time
import TouchScreenGUI as tsgui
from multiprocessing import Process, Queue
import subprocess

class Supervisor(object):

    def __init__(self):
        self.guiQueue = Queue()
        self.handlerQueue = Queue()
        self.readerQueue = Queue()
        self.statusQueue = Queue()
    
    def startReader(self):
        #self.readerQueue.put("run")
        reader = Reader.Reader(self.readerQueue)
        reader.run()
    
    def startHandler(self):
        #self.handlerQueue.put("run")
        handler = Handler.Handler(self.handlerQueue)
        handler.run()
        
    def startGUI(self):
        myGui = tsgui.FrontEnd(self.guiQueue, self.statusQueue)
        myGui.run()
    
    def run(self):
        print "Supervisor, checking in! pid:", os.getpid()
        # If image directory does not exist yet, create it!
        config = Utility.getProjectConfig()
        imgdir = config.get('directories','imagedirectory')
        if not os.path.isdir(imgdir):
            try:
                os.makedirs(imgdir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        guiProcess = Process(target = self.startGUI)
        guiProcess.start()
        # Initialize with all images currently on camera
        self.statusQueue.put(Utility.QMSG_SCAN)
        # BUG: CRASHING BECAUSE IT CAN'T FIND FILE, EVEN WHEN EXISTS; NEEDS INVESTIGATION
        Reader.camera_filenames_to_file(Utility.OLD_PICS_FILE_NAME)
        self.statusQueue.put(Utility.QMSG_SCAN_DONE)
        time.sleep(Utility.POLL_TIME)
        self.statusQueue.put(Utility.QMSG_IDLE)    
        handlerProcess = None
        readerProcess = None
        while True:
            if not self.guiQueue.empty():
                job = self.guiQueue.get()
                if job == Utility.QMSG_START:
                    print "Supervisor handles Upload job here"
                    readerProcess = Process(target = self.startReader)
                    self.readerQueue.put(Utility.QMSG_SCAN)
                    self.statusQueue.put(Utility.QMSG_SCAN)
                    readerProcess.start()
                    # wait for reader to finish scanning
                    readerProcess.join()
                    self.statusQueue.put(Utility.QMSG_SCAN_DONE)
                     
                    # THIS MIGHT WORK, DEPENDING ON DESIGN OF READER
                    # alternatively we scan the self.readerQueue for QMSG_SCAN_DONE
                    handlerProcess = Process(target = self.startHandler)
                    self.handlerQueue.put(Utility.QMSG_HANDLE)
                    handlerProcess.start()
                elif job == Utility.QMSG_SETTINGS:
                    print "Supervisor handles Settings job here if needed"
                elif job == Utility.QMSG_FILE_EXPLORER:
                    pass
                else:
                    raise Exception('Supervisor.run:  unexpected object in queue')
            # endif self.guiQueue.empty()
            
            time.sleep(1) # wait for handlerProcess to actually start
            if self.handlerQueue.empty():
                print 'handlerQueue still empty'
            else:
                handlerMsg = Utility.readMessageQueue(self.handlerQueue) 
                if handlerMsg == Utility.QMSG_UPLOAD:
                    self.statusQueue.put(Utility.QMSG_UPLOAD)
                    
                elif handlerMsg == Utility.QMSG_UPLOAD_DONE:
                    self.statusQueue.put(Utility.QMSG_UPLOAD_DONE)
                elif handlerMsg == Utility.QMSG_HANDLE_NONE:
                    self.statusQueue.put(Utility.QMSG_HANDLE_NONE)
                else:
                    self.statusQueue.put("Unknown Message from handlerQueue")
            time.sleep(Utility.POLL_TIME)
        # end while loop
    
if __name__ == '__main__':
    Supervisor().run()
    
        
