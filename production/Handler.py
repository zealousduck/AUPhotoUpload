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
        os.chdir(self.directoryName)
        self.queue = Queue()
        
    def run(self):
        print "Hi, I'm a Handler!"
        print "Starting Uploader!"
        uploaderProcess = Process(target = self.startUploader)
        uploaderProcess.start()
        time.sleep(1.5)
        while True:
            time.sleep(constants.POLL_TIME)
            print "Handler, checking in!"
        uploaderProcess.join()
    
    def enqueue(self):
        pass
    
    def startUploader(self):
        uploader = Uploader.Uploader(self.queue)
        uploader.run()
        pass