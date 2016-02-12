'''
Created on Feb 3, 2016

Uploader.py class uploads queued images to Dropbox with its API.
'''
import PhotoUploadConstants as constants
import PhotoUploadUtility as Utility
import multiprocessing
import os
import time
#import dropbox

class Uploader(object):

    def __init__(self, q=None):
        if q is None:
            raise Exception('Uploader.__init__():  missing parameter')
        if not isinstance(q, multiprocessing.queues.Queue):
            raise Exception('Uploader.__init__():  parameter not of type ""')
        self.queue = q
        config = Utility.getProjectConfig()
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
        # INSERT DROPBOX DATA FROM CONFIG HERE
    
    def run(self):
        print "Hi, I'm an Uploader!"
        time.sleep(1)
        while True:
            time.sleep(constants.POLL_TIME)
            print "Uploader, checking in! pid:", os.getpid()
    
    def dequeue(self):
        return self.queue.get()
    
    def uploadFile(self):
        pass
    
    def uploadBatch(self):
        pass
        