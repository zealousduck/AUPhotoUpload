'''
Created on Feb 28, 2016

@author: chris
'''
import subprocess as sb
import os
import time

class CamReader(object):
    '''
    classdocs
    '''
    shell = False;
    dirPhoto = "~/Pictures/Dropbox"
    dirThumb = "~/Pictures/Thumbnail"
    dirBrowser = "~/Picture/Browser"

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def wait_event_download(self):
        try:
            # Adds pictures to the stored photo directory. If no camera is supported, we raise an error.
            sb.check_output(["gphoto2", "--wait-event-and-download", "--skip-existing", self.dirBrowser], self.shell);
        except sb.CalledProcessError:
            print "Camera is either not connected or not supported"
    
    def toggle_off(self):
        try:
            sb.check_output(["killall", "gphoto2"], self.shell);
        except sb.CalledProcessError:
            print "Gphoto2 not a running proccess."
            
        finally:
            exit        

#main test
read = CamReader();
read.wait_event_download();
#read.toggle_off()