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
        self.userInputQueue = Queue()
        self.handlerQueue = Queue()
        self.readerQueue = Queue()
        self.statusQueue = Queue()
        self.readerProcess = None
        self.handlerProcess = None
        self.didScanFail = False
        self.stableInternet = False
        self.handlerDelayed = False
        self.stableInternetCounter = 0
    
    '''
    startGUI() initializes and runs the GUI. It is started once and only
        terminated at the end of the program execution. Messages can be passed
        to the GUI via self.statusQueue so that the Supervisor can update the GUI
        based on background work. Messages are passed back to the Supervisor via
        self.userInputQueue, based on GUI button presses. 
        startGUI() is intended to be hooked into a multiprocessing Process() call.
    '''    
    def startGUI(self):
        myGui = tsgui.FrontEnd(self.userInputQueue, self.statusQueue)
        myGui.run()
    
    '''
    startReader() initializes and runs the Reader. It is started at the beginning
        of every workflow, when the User presses "Start Upload". Messages can be
        passed to and from the Reader via self.readerQueue.
    '''
    def startReader(self):
        reader = Reader.Reader(self.readerQueue)
        reader.run()
        
    '''
    runReader() starts the Reader process and manages the QMSG orders placed in
        both the Reader queue and the GUI status queue.
    '''
    def runReader(self):
        self.readerProcess = Process(target = self.startReader)
        self.readerQueue.put(Utility.QMSG_SCAN)
        self.statusQueue.put(Utility.QMSG_SCAN)
        self.readerProcess.start()
        self.readerProcess.join()
        
    '''
    startHandler() initializes and runs the Handler. It is started after the Reader
        in the workflow. Messages can be passed to and from the Handler via 
        self.handlerQueue.
    '''
    def startHandler(self):
        handler = Handler.Handler(self.handlerQueue, self.statusQueue)
        handler.run()
            
    '''
    runHandler() starts the Handler process and manages the QMSG orders placed
        in the Handler's queue. It additionally marks that Handler processing has
        begun.
    '''
    def runHandler(self):
        self.handlerProcess = Process(target = self.startHandler)
        self.handlerQueue.put(Utility.QMSG_HANDLE)
        self.handlerProcess.start()
        
    '''
    verifyImageDirectory() makes sure that the program can access the necessary
        directory for the images it is handling. If it does not exist, it will
        create it.
    '''
    def verifyImageDirectory(self):
        config = Utility.getProjectConfig()
        imgdir = config.get('directories','imagedirectory')
        print imgdir
        if not os.path.isdir(imgdir):
            try:
                os.makedirs(imgdir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise Exception('failed to create image directory')     
    
    '''
    initializeInternet() establishes whether the program has internet connectivity
        at program start-up. The GUI will be updated accordingly.
    '''
    def initializeInternet(self):
        self.stableInternetCounter = 0
        for i in range(Utility.STABLE_INTERNET_COUNT + Utility.STABLE_INTERNET_COUNT/2):
            if (Utility.checkInternetConnection() 
                    and self.stableInternetCounter < Utility.STABLE_INTERNET_COUNT):
                self.stableInternetCounter += 1
        if (self.stableInternetCounter >= Utility.STABLE_INTERNET_COUNT):
            self.statusQueue.put(Utility.QMSG_IDLE)
            self.stableInternet = True
        else:
            self.statusQueue.put(Utility.QMSG_INTERNET_NO)
            self.stableInternet = False
    
    '''
    updateInternet() periodically checks whether the internet is stable enough
        to be used. self.stableInternetCounter acknowledges the potential
        for time-outs and instead allows some rubber-banding of connectivity.
    '''
    def updateInternet(self):
        if Utility.checkInternetConnection():
            if (self.stableInternetCounter < Utility.STABLE_INTERNET_COUNT):
                self.stableInternetCounter += 1
            if (self.stableInternetCounter >= Utility.STABLE_INTERNET_COUNT):
                self.stableInternet = True
                self.statusQueue.put(Utility.QMSG_INTERNET_YES)
                #print 'DEBUG: checkInternetConnection() == True'
        else:
            if (self.stableInternetCounter > 0): # only count down to 0
                self.stableInternetCounter -= 1 
            if (self.stableInternetCounter < Utility.STABLE_INTERNET_COUNT/2):
                self.stableInternet = False
                self.statusQueue.put(Utility.QMSG_INTERNET_NO)
                #print 'DEBUG: checkInternetConnection() == False'
        #print 'DEBUG: stableInternet:', self.stableInternet, 'stableInternetCounter:', self.stableInternetCounter
    
    '''
    tryScan() implements an alternative workflow for Supervisor that does not
        pull any images from the camera or upload anything. Instead, it enables
        Supervisor to establish a "baseline" for images to compare to. tryScan()
        is intended for when camera connectivity is faulty, resulting in 
        corrupt or missing baselines.
        A baseline for images is necessary, otherwise every image on the camera
        will be uploaded!
    '''
    def tryScan(self):
        try:
            self.statusQueue.put(Utility.QMSG_SCAN)
            Reader.camera_filenames_to_file(Utility.OLD_PICS_FILE_NAME)
            self.statusQueue.put(Utility.QMSG_SCAN_DONE)
            self.didScanFail = False
        except:
            self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
            self.didScanFail = True
            
    '''
    isScanMessageFail() is a boolean function that checks whether a camera scan
        is faulty (in conjunction with tryScan()). The results of the scan are
        pushed to the GUI for display. This function returns True if the scan
        fails, and False otherwise.
    '''
    def isScanMessageFail(self):
        messageStatus = False
        scanMsg = Utility.readMessageQueue(self.readerQueue)
        if scanMsg == Utility.QMSG_SCAN_FAIL:
            self.statusQueue.put(Utility.QMSG_SCAN_FAIL)
            messageStatus = True # failed, tell GUI but ignore the rest of this job
            self.didScanFail = True
        elif scanMsg == Utility.QMSG_SCAN_DONE:
            self.statusQueue.put(Utility.QMSG_SCAN_DONE)
            self.didScanFail = False
        else:
            print "Something went wrong with the ReaderMsgQueue!"
            messageStatus = False
        return messageStatus
    
    '''
    processHandlerMsg() retrieves messages from the Handler queue since 
        Handler(Uploader) processing occurs in the background, with the chance
        to regularly send the Supervisor status updates. This function retrieves
        and passes those messags onto the GUI.
    '''
    def processHandlerMsg(self):
        if not self.handlerQueue.empty():
            handlerMsg = Utility.readMessageQueue(self.handlerQueue) 
            if handlerMsg == Utility.QMSG_UPLOAD:
                self.statusQueue.put(Utility.QMSG_UPLOAD) 
            elif handlerMsg == Utility.QMSG_UPLOAD_DONE:
                self.statusQueue.put(Utility.QMSG_UPLOAD_DONE)
            elif handlerMsg == Utility.QMSG_HANDLE_NONE:
                self.statusQueue.put(Utility.QMSG_HANDLE_NONE)
            elif handlerMsg == QMSG_UPLOAD_USER_FAIL:
                self.statusQueue.put(QMSG_UPLOAD_USER_FAIL)
            elif handlerMsg == QMSG_UPLOAD_IMAGE_FAIL:
                self.statusQueue.put(QMSG_UPLOAD_IMAGE_FAIL)
            else:
                self.statusQueue.put("Unknown Message from handlerQueue")
    
    '''
    startUploadJob() is the "normal" workflow for when the user desires to 
        pull images from the camera and upload them. It makes sure to only
        activate Handler if the scan is successful.
    '''
    def printQueue(self, toPrintQueue):
        print "Printing Queue"
        time.sleep(1)
        sizeyQueue = Queue()
        sizey =  toPrintQueue.qsize()
        for i in range(0, sizey):
            watDaFug = toPrintQueue.get()
            print watDaFug
            sizeyQueue.put(watDaFug)
        for i in range(0, sizey):
            toPrintQueue.put(sizeyQueue.get())
        time.sleep(1)
    
    def startUploadJob(self):
        self.runReader()
        if not self.isScanMessageFail(): 
            print 'scan does not fail!'
            if self.stableInternet: # only start Handler if stable connection
                self.handlerQueue.put(Utility.QMSG_HANDLE)
                self.runHandler()
                print 'handler run!'
                self.handlerDelayed = False
            else:
                print 'handler not run!'
                time.sleep(Utility.POLL_TIME)
                self.handlerDelayed = True
    
    '''
    run() is the entry-point and main loop for the PhotoUpload program.
        run() is where the Supervisor coordinates the various children and workflow
        activities.
        Write something more descriptive here later?
    '''
    def run(self):
        self.verifyImageDirectory()
        Process(target = self.startGUI).start()
        self.initializeInternet()
        self.tryScan()
        time.sleep(Utility.POLL_TIME)
        while True:
            if not self.userInputQueue.empty():
                
                #self.printQueue(self.handlerQueue)
                job = self.userInputQueue.get()
                if (job == Utility.QMSG_START and self.didScanFail):
                    print 'tryScan()'
                    self.tryScan()
                elif (job == Utility.QMSG_START and not self.didScanFail):
                    print 'startUploadJob()'
                    self.startUploadJob()
                elif (job == Utility.QMSG_SETTINGS):
                    print "Supervisor handles Settings job here if needed"
                else:
                    raise Exception('Supervisor.run:  unexpected object in queue')
            # endif self.userInputQueue.empty()
            #self.printQueue(self.handlerQueue)
            if self.handlerDelayed and self.stableInternet:
                self.handlerDelayed = False
                self.runHandler()
            self.processHandlerMsg()
            self.updateInternet()
            time.sleep(Utility.POLL_TIME)
        # end while loop
    
if __name__ == '__main__':
    if not os.path.isfile(Utility.CONFIG_FILE_NAME):
        Configurer.Configurer().revertToDefaults()
    Supervisor().run()

        
