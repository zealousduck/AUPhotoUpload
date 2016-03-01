'''
Created on Feb 28, 2016

@author: chris
'''
import subprocess as sb
import os

class CamReader(object):
    '''
    classdocs
    '''
    shell = True;
    curPID = None;
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
            # Here we need to figure out proper error handling
            self.wait_event_download(); #Continues to attempt the connection in till killed
                
            
        self.curPID = os.getpid(); #Use this pid to toggle off. Using kill.
        #print self.curPID;
    
    def toggle_off(self):
        try:
            sb.check_output(["kill", self.curPID], self.shell);
        except sb.CalledProcessError:
                self.toggle_off() #run intill dead

#main test
read = CamReader();
read.wait_event_download();