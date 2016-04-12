'''
Created on Feb 3, 2016

Supervisor.py is the parent class and entry point for the PhotoUpload
    application. It creates the child classes that perform the work.
    Direct child processes: Reader, Handler
'''
import PhotoUploadUtility as Utility
import Reader
import Handler
import Configurer
import os
import errno
import time
import TouchScreenGUI as tsgui
from multiprocessing import Process, Queue

class Supervisor(object):

    def __init__(self):
        self.guiQueue = Queue()
        self.handlerQueue = Queue()
        self.readerQueue = Queue()
        self.statusQueue = Queue()
    
    def startReader(self):
        reader = Reader.Reader(self.readerQueue)
        reader.run()
    
    def startHandler(self):
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
        print imgdir
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
        Reader.camera_filenames_to_file(Utility.OLD_PICS_FILE_NAME)
        self.statusQueue.put(Utility.QMSG_SCAN_DONE)
        time.sleep(Utility.POLL_TIME)
        # Establish whether we have stable internet
        stableInternetCounter = 0
        stableInternet = False  
        for i in range(2*Utility.STABLE_INTERNET_COUNT):
            if Utility.checkInternetConnection():
                stableInternetCounter += 1
        if (stableInternetCounter == Utility.STABLE_INTERNET_COUNT):
            self.statusQueue.put(Utility.QMSG_IDLE)
            stableInternet = True
        else:
            self.statusQueue.put(Utility.QMSG_INTERNET_NO)
            stableInternet = False
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
                    
                    if stableInternet: # only start Handler if stable connection
                        handlerProcess = Process(target = self.startHandler)
                        self.handlerQueue.put(Utility.QMSG_HANDLE)
                        handlerProcess.start()
                    else:
                        time.sleep(Utility.POLL_TIME)
                        self.statusQueue.put(Utility.QMSG_INTERNET_NO)
                elif job == Utility.QMSG_SETTINGS:
                    print "Supervisor handles Settings job here if needed"
                else:
                    raise Exception('Supervisor.run:  unexpected object in queue')
            # endif self.guiQueue.empty()
            
            time.sleep(Utility.POLL_TIME) # wait for handlerProcess to actually start
            if not self.handlerQueue.empty():
                handlerMsg = Utility.readMessageQueue(self.handlerQueue) 
                if handlerMsg == Utility.QMSG_UPLOAD:
                    self.statusQueue.put(Utility.QMSG_UPLOAD) 
                elif handlerMsg == Utility.QMSG_UPLOAD_DONE:
                    self.statusQueue.put(Utility.QMSG_UPLOAD_DONE)
                elif handlerMsg == Utility.QMSG_HANDLE_NONE:
                    self.statusQueue.put(Utility.QMSG_HANDLE_NONE)
                else:
                    self.statusQueue.put("Unknown Message from handlerQueue")
            
            # Check current internet connection, allowing for some fluctuation
            if Utility.checkInternetConnection():
                if not stableInternetCounter == Utility.STABLE_INTERNET_COUNT:
                    stableInternetCounter += 1
                else:
                    stableInternet = True
                print 'DEBUG: checkInternetConnection() == True'
            else:
                stableInternetCounter -= 1
                if stableInternetCounter < Utility.STABLE_INTERNET_COUNT/2:
                    stableInternet = False
                    self.statusQueue.put(Utility.QMSG_INTERNET_NO)
                print 'DEBUG: checkInternetConnection() == False'
            print 'DEBUG: stableInternet:', stableInternet    
        
            time.sleep(Utility.POLL_TIME)
        # end while loop
    
if __name__ == '__main__':
    if not os.path.isfile(Utility.CONFIG_FILE_NAME):
        Configurer.Configurer().revertToDefaults()
    Supervisor().run()

        