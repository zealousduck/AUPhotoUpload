'''
Created on Feb 3, 2016

Reader.py class interacts directly with the camera through gphoto2. New
    photos are automatically inserted into a designated directory.
'''
import PhotoUploadUtility as Utility
import time
import os
import subprocess
from Queue import Queue

class Reader(object):

    def __init__(self, orders):
        config = Utility.getProjectConfig()
        self.myOrders = orders
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
    
    def run(self):
        print "Hi, I'm a Reader!"
        status = Utility.readMessageQueue(self.myOrders)
        if status == Utility.QMSG_SCAN:
            pass # READER SCAN PATCH INSERTED LOGIC HERE 
        print "Reader is exiting."
        # Put actual cleanup/saving code here!
        print "Reader successfully exited."
    
    def wait_event_download(self):
        try:
            # Adds pictures to the stored photo directory. If no camera is supported, we raise an error.
            subprocess.check_output(["gphoto2", "--wait-event-and-download", "--skip-existing", self.dirBrowser], self.shell)
        except subprocess.CalledProcessError:
            print "Camera is either not connected or not supported"
        
    def toggle_off(self):
        try:
            subprocess.check_output(["killall", "gphoto2"], self.shell)
        except subprocess.CalledProcessError:
            print "Gphoto2 not a running proccess."    
        finally:
            exit  
            
            
            
