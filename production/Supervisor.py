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
        # Establish whether we have stable internet
        stableInternetCounter = 0
        stableInternet = False  
        for i in range(Utility.STABLE_INTERNET_COUNT):
            if Utility.checkInternetConnection():
                stableInternetCounter += 1
        if (stableInternetCounter >= Utility.STABLE_INTERNET_COUNT):
            self.statusQueue.put(Utility.QMSG_IDLE)
            stableInternet = True
        else:
            self.statusQueue.put(Utility.QMSG_INTERNET_NO)
            stableInternet = False
        # Initialize with all images currently on camera
        self.statusQueue.put(Utility.QMSG_SCAN)
        initialScanFail = True
        try:
            Reader.camera_filenames_to_file(Utility.OLD_PICS_FILE_NAME)
            self.statusQueue.put(Utility.QMSG_SCAN_DONE)
            initialScanFail = False
        except:
            self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
            initialScanFail = True
        time.sleep(Utility.POLL_TIME)
        handlerProcess = None
        handlerDelayed = False
        readerProcess = None
        while True:
            if not self.guiQueue.empty():
                job = self.guiQueue.get()
                if job == Utility.QMSG_START:
                    if initialScanFail:
                        try: # OH GOD PLEASE REFACTOR THIS DUPLICATED CODE !!!!!!!!!!!!!!
                            Reader.camera_filenames_to_file(Utility.OLD_PICS_FILE_NAME)
                            self.statusQueue.put(Utility.QMSG_SCAN_DONE)
                            initialScanFail = False
                        except:
                            self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
                            initialScanFail = True
                        continue # cannot complete job as normal if no baseline scan
                        # REFACTOR THIS CODE, DON'T FORGET! try Supervisor.initialScan()
                    print "Supervisor handles Upload job here"
                    readerProcess = Process(target = self.startReader)
                    self.readerQueue.put(Utility.QMSG_SCAN)
                    self.statusQueue.put(Utility.QMSG_SCAN)
                    readerProcess.start()
                    # wait for reader to finish scanning
                    readerProcess.join()
                    scanMsg = Utility.readMessageQueue(self.readerQueue)
                    if scanMsg == Utility.QMSG_SCAN_FAIL:
                        self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
                        scanMsg = 0 
                        continue # failed, tell GUI but ignore the rest of this job
                    elif scanMsg == Utility.QMSG_SCAN_DONE:
                        self.statusQueue.put(Utility.QMSG_SCAN_DONE)
                        scanMsg = 0
                    else:
                        print "Something went wrong with the ReaderMsgQueue!"
                    if stableInternet: # only start Handler if stable connection
                        handlerProcess = Process(target = self.startHandler)
                        self.handlerQueue.put(Utility.QMSG_HANDLE)
                        handlerProcess.start()
                        handlerDelayed = False
                    else:
                        time.sleep(Utility.POLL_TIME)
                        self.statusQueue.put(Utility.QMSG_INTERNET_NO)
                        handlerDelayed = True
                elif job == Utility.QMSG_SETTINGS:
                    print "Supervisor handles Settings job here if needed"
                else:
                    raise Exception('Supervisor.run:  unexpected object in queue')
            # endif self.guiQueue.empty()
            
            # Start upload if delayed and internet is now stable
            if handlerDelayed and stableInternet:
                handlerProcess = Process(target = self.startHandler)
                self.handlerQueue.put(Utility.QMSG_HANDLE)
                handlerProcess.start()
                handlerDelayed = False   
            
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
            
            # Check current internet connection, allowing for some fluctuation in results
            if Utility.checkInternetConnection():
                if stableInternetCounter < Utility.STABLE_INTERNET_COUNT:
                    stableInternetCounter += 1
                else:
                    stableInternet = True
                    self.statusQueue.put(Utility.QMSG_INTERNET_YES)
                #print 'DEBUG: checkInternetConnection() == True'
            else:
                if (stableInternetCounter > 0): # only count down to 0
                    stableInternetCounter -= 1 
                if stableInternetCounter < Utility.STABLE_INTERNET_COUNT/2:
                    stableInternet = False
                    self.statusQueue.put(Utility.QMSG_INTERNET_NO)
                #print 'DEBUG: checkInternetConnection() == False'
            print 'DEBUG: stableInternet:', stableInternet, 'stableInternetCounter:', stableInternetCounter    
        
            time.sleep(Utility.POLL_TIME)
        # end while loop
    
if __name__ == '__main__':
    if not os.path.isfile(Utility.CONFIG_FILE_NAME):
        Configurer.Configurer().revertToDefaults()
    Supervisor().run()

        