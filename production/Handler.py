'''
Created on Feb 3, 2016

Handler.py class operates on the designated directory to determine new images
    to be uploaded. Spawns the child process Uploader and communicates the
    images to be uploaded by placing the image names in a shared queue.
'''
import PhotoUploadConstants as constants
import ConfigParser
import Uploader
from multiprocessing import Process, Queue
import time
import os

class Handler(object):

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        if os.path.isfile(constants.CONFIG_FILE_NAME):
            config.read(constants.CONFIG_FILE_NAME)
        else:
            config.read(constants.DEFAULT_CONFIG)
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
        
    def run(self):
        print "Hi, I'm a Handler!"
        time.sleep(1.5)
        while True:
            time.sleep(constants.POLL_TIME)
            print "Handler, checking in!"
    
    def enqueue(self):
        pass
    
    def startUploader(self):
        pass