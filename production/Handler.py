'''
Created on Feb 3, 2016

Handler.py class operates on the designated directory to determine new images
    to be uploaded. Spawns the child process Uploader and communicates the
    images to be uploaded by placing the image names in a shared queue.
'''
import PhotoUploadConstants as constants
import PhotoUploadUtility as Utility
import Uploader
from multiprocessing import Process, Queue
import time
import os

class Handler(object):

    def __init__(self):
        config = Utility.getProjectConfig()
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        
        self.queue = Queue()
        self.imageList = self.getDirectoryList(self.directoryName)
        
    def run(self):
        print "Hi, I'm a Handler!"
        print "Starting Uploader!"
        uploaderProcess = Process(target = self.startUploader)
        uploaderProcess.start()
        print self.directoryName
        while True:
            currentList = self.getDirectoryList(self.directoryName)
            listToUpload = self.getListDifference(self.imageList, currentList)
            if len(listToUpload) != 0:
                for element in listToUpload:
                    self.enqueue(element)
            self.imageList = self.getDirectoryList(self.directoryName)
            print "Current list:", self.imageList
            time.sleep(constants.POLL_TIME)
        uploaderProcess.join()
    
    def enqueue(self, element=None):
        if element is None:
            raise Exception('Handler.enqueue():  missing parameter')
        self.queue.put(element)
    
    def startUploader(self):
        uploader = Uploader.Uploader(self.queue)
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
    
