'''
Created on Feb 3, 2016

Reader.py class interacts directly with the camera through gphoto2. New
    photos are automatically inserted into a designated directory.
'''
import PhotoUploadConstants as constants
import PhotoUploadUtility as Utility
import time
import os

class Reader(object):

    def __init__(self, orders):
        config = Utility.getProjectConfig()
        self.myOrders = orders
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
    
    def run(self):
        print "Hi, I'm a Reader!"
        while not self.myOrders.empty():
            time.sleep(constants.POLL_TIME)
            print "Reader, checking in! pid:", os.getpid()
            # Plug in actual functionality from prototypes!
        print "Reader is exiting."
        
        print "Reader successfully exited."
    
    
