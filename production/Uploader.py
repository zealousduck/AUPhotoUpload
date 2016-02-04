'''
Created on Feb 3, 2016

Uploader.py class uploads queued images to Dropbox with its API.
'''
import PhotoUploadConstants as constants
import ConfigParser
from multiprocessing import Queue
import os
#import dropbox

class Uploader(object):

    def __init__(self, queue=None):
        if queue is None:
            raise Exception('Uploader:  missing queue')
        self.queue = queue
        config = ConfigParser.RawConfigParser()
        if os.path.isfile(constants.CONFIG_FILE_NAME):
            config.read(constants.CONFIG_FILE_NAME)
        else:
            config.read(constants.DEFAULT_CONFIG)
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
        # INSERT DROPBOX DATA FROM CONFIG HERE
    
    def run(self):
        print "Hi, I'm an Uploader!"
        pass
    
    def dequeue(self):
        pass
    
    def uploadFile(self):
        pass
    
    def uploadBatch(self):
        pass
        