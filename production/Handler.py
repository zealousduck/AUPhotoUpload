'''
Created on Feb 3, 2016

Handler.py class operates on the designated directory to determine new images
    to be uploaded. Spawns the child process Uploader and communicates the
    images to be uploaded by placing the image names in a shared queue.
'''
import PhotoUploadUtility as Utility
import Uploader
from multiprocessing import Process, Queue
import time
import os
import datetime
import subprocess

class Handler(object):

    def __init__(self, orderQueue):
        config = Utility.getProjectConfig()
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        self.orders = orderQueue
        self.uploadOrders = Queue()
        self.queue = Queue()
        self.listFileName = Utility.UPLOADS_FILE_NAME
        self.exitMessage = ""
        
#     def run(self):
#         print "Hi, I'm a Handler!"
#         print "Starting Uploader!"
#         self.uploadOrders.put("run")
#         uploaderProcess = Process(target = self.startUploader)
#         uploaderProcess.start()
#         print self.directoryName
#         while not self.orders.empty():
#             currentList = self.getDirectoryList(self.directoryName)
#             listToUpload = self.getListDifference(self.imageList, currentList)
#             if len(listToUpload) != 0:
#                 for element in listToUpload:  
#                     self.enqueue(self.renameWithTimestamp(element)) # rename and submit the renamed image name
#                     #self.enqueue(element)
#             self.imageList = self.getDirectoryList(self.directoryName)
#             print "Current list:", self.imageList
#             time.sleep(Utility.POLL_TIME)
#         print "Handler is exiting."
#         # Put actual cleanup/saving code here!
#         self.uploadOrders.get() #Tells the Uploader process to finish
#         uploaderProcess.join() #Waits for the Uploader process to finish
#         print "Handler successfully exited."
        
    def run(self):
        status = Utility.readMessageQueue(self.orders)
        if status == Utility.QMSG_HANDLE:
            oldList = []
            # pull the old list from disk, if it exists
            if os.path.isfile(self.listFileName):
                f = open(self.listFileName, 'r')
                for line in f:
                    oldList.append(line[:-1]) #ignore '/n' when read in
                f.close()
            # compare to current directory
            currentList = self.getDirectoryList(self.directoryName)
            listToUpload = self.getListDifference(oldList, currentList)
            renamedList = []
            for element in listToUpload:
                renamedList.append(self.renameWithTimestamp(element))
            if len(listToUpload) != 0:
                self.exitMessage = Utility.QMSG_UPLOAD_DONE
                f = open(self.listFileName, 'a')
                for element in renamedList:  
                    self.enqueue(element) # rename and submit the renamed image name
                    f.write(element + '\n')
                f.close()
                uploaderProcess = Process(target = self.startUploader)
                self.uploadOrders.put(Utility.QMSG_UPLOAD)
                uploaderProcess.start()
                
                self.orders.put(Utility.QMSG_UPLOAD)
                # then enqueued, wait for uploader to finish
                uploaderProcess.join()
            else:
                self.exitMessage = Utility.QMSG_HANDLE_NONE
            
        # once uploader done, exit/send a message to supervisor "done" and then exit
        self.orders.put(self.exitMessage)
    
    def enqueue(self, element=None):
        if element is None:
            raise Exception('Handler.enqueue():  missing parameter')
        self.queue.put(element)
    
    def startUploader(self):
        uploader = Uploader.Uploader(self.queue, self.uploadOrders)
        uploader.run()

    def getDirectoryList(self, path=None):
        if (path is None):
            return None
        directoryList = []
        for item in os.listdir(path):
            directoryList.append(item)
        return directoryList
    
    def getListDifference(self, oldList, newList):
        differenceList = []
        for element in newList:
            if (element not in oldList): # verify correctness for strings!!!
                differenceList.append(element)
        return differenceList
    
    def renameWithTimestamp(self, name):
        fileExtension = os.path.splitext(name)[1] # os.path.splitext(name)[1] returns the file extension
        i = str(datetime.datetime.now())
        # Convert '2016-02-08 11:16:04.123456 format to nicer filename
        timeStamp = i[0:10] + '-' + i[11:13] + '-' + i[14:16] + '-' + i[17:19]
        
        newName = (timeStamp + fileExtension)
        newPath = (self.directoryName + '/' + newName)
        
        counter = 0
        counterExtension = ''
        
        while os.path.isfile(newPath):
            counter += 1
            counterExtension = '-' + str(counter)
            newName = (timeStamp + counterExtension + fileExtension)
            newPath = (self.directoryName + '/' + newName)
        os.rename(self.directoryName + '/' + name, newPath)
        #subprocess.call(['mv', (self.directoryName + '/' + name), newPath])
        return newName

    
