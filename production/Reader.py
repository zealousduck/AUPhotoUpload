'''
Created on Feb 3, 2016

Reader.py class interacts directly with the camera through gphoto2. New
    photos are automatically inserted into a designated directory.
'''
import PhotoUploadConstants as constants
import ConfigParser
import time
import os

class Reader(object):

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
        print "Hi, I'm a Reader!"
        while True:
            time.sleep(constants.POLL_TIME)
            print "Reader, checking in!"
            
    
    