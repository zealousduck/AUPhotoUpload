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
        self.readerProcess = None
        self.handlerProcess = None
        self.didScanFail = False
        self.stableInternet = False
        self.handlerDelayed = False
        self.stableInternetCounter = 0
    
    def startReader(self):
        reader = Reader.Reader(self.readerQueue)
        reader.run()
        
    def runReader(self):
        self.readerProcess = Process(target = self.startReader)
        self.readerQueue.put(Utility.QMSG_SCAN)
        self.statusQueue.put(Utility.QMSG_SCAN)
        self.readerProcess.start()
        # wait for reader to finish scanning
        self.readerProcess.join()
        
    def startHandler(self):
        handler = Handler.Handler(self.handlerQueue)
        handler.run()
        
    def runHandler(self):
        self.handlerProcess = Process(target = self.startHandler)
        self.handlerQueue.put(Utility.QMSG_HANDLE)
        self.handlerProcess.start()
        self.handlerDelayed = False
        
    def startGUI(self):
        myGui = tsgui.FrontEnd(self.guiQueue, self.statusQueue)
        myGui.run()
        
    def createImageDir(self):
        config = Utility.getProjectConfig()
        imgdir = config.get('directories','imagedirectory')
        print imgdir
        if not os.path.isdir(imgdir):
            try:
                os.makedirs(imgdir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        
        
    def checkInternet(self):
        self.stableInternetCounter = 0
        for i in range(Utility.STABLE_INTERNET_COUNT):
            if Utility.checkInternetConnection():
                self.stableInternetCounter += 1
        if (self.stableInternetCounter >= Utility.STABLE_INTERNET_COUNT):
            self.statusQueue.put(Utility.QMSG_IDLE)
            self.stableInternet = True
        else:
            self.statusQueue.put(Utility.QMSG_INTERNET_NO)
            self.stableInternet = False
            
    def updateInternet(self):
        if Utility.checkInternetConnection():
            if self.stableInternetCounter < Utility.STABLE_INTERNET_COUNT:
                self.stableInternetCounter += 1
            else:
                self.stableInternet = True
                self.statusQueue.put(Utility.QMSG_INTERNET_YES)
                #print 'DEBUG: checkInternetConnection() == True'
        else:
            if (self.stableInternetCounter > 0): # only count down to 0
                self.stableInternetCounter -= 1 
            if self.stableInternetCounter < Utility.STABLE_INTERNET_COUNT/2:
                self.stableInternet = False
                self.statusQueue.put(Utility.QMSG_INTERNET_NO)
                #print 'DEBUG: checkInternetConnection() == False'
        print 'DEBUG: stableInternet:', self.stableInternet, 'stableInternetCounter:', self.stableInternetCounter
        
    def tryScan(self):
        try:
            Reader.camera_filenames_to_file(Utility.OLD_PICS_FILE_NAME)
            self.statusQueue.put(Utility.QMSG_SCAN_DONE)
            self.didScanFail = False
        except:
            self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
            self.didScanFail = True
            
    def isScanMessageFail(self):
        messageStatus = False
        scanMsg = Utility.readMessageQueue(self.readerQueue)
        if scanMsg == Utility.QMSG_SCAN_FAIL:
            self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
            messageStatus = True # failed, tell GUI but ignore the rest of this job
        elif scanMsg == Utility.QMSG_SCAN_DONE:
            self.statusQueue.put(Utility.QMSG_SCAN_DONE)
        else:
            print "Something went wrong with the ReaderMsgQueue!"
        return messageStatus
    
    def processHandlerMsg(self):
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
    
    def run(self):
        print "Supervisor, checking in! pid:", os.getpid()
        # If image directory does not exist yet, create it!
        
        
        self.createImageDir()
        guiProcess = Process(target = self.startGUI)
        guiProcess.start()
        # Establish whether we have stable internet
        self.checkInternet()
        # Initialize with all images currently on camera
        self.statusQueue.put(Utility.QMSG_SCAN)
        self.tryScan()
        time.sleep(Utility.POLL_TIME)
        while True:
            if not self.guiQueue.empty():
                job = self.guiQueue.get()
                if job == Utility.QMSG_START:
                    if self.didScanFail:
                        self.tryScan()
                        continue # cannot complete job as normal if no baseline scan
                        # REFACTOR THIS CODE, DON'T FORGET! try Supervisor.initialScan()
                    print "Supervisor handles Upload job here"
                    self.runReader()
                    if self.isScanMessageFail():
                        continue
                    if self.stableInternet: # only start Handler if stable connection
                        self.runHandler()
                    else:
                        time.sleep(Utility.POLL_TIME)
                        self.handlerDelayed = True
                elif job == Utility.QMSG_SETTINGS:
                    print "Supervisor handles Settings job here if needed"
                else:
                    raise Exception('Supervisor.run:  unexpected object in queue')
            # endif self.guiQueue.empty()
            
            # Start upload if delayed and internet is now stable
            if self.handlerDelayed and self.stableInternet:
                self.runHandler()
            
            time.sleep(Utility.POLL_TIME) # wait for handlerProcess to actually start
            self.processHandlerMsg()
            
            # Check current internet connection, allowing for some fluctuation in results    
            self.updateInternet()
            time.sleep(Utility.POLL_TIME)
        # end while loop
    
if __name__ == '__main__':
    if not os.path.isfile(Utility.CONFIG_FILE_NAME):
        Configurer.Configurer().revertToDefaults()
    Supervisor().run()

        
