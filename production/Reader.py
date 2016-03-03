'''
Created on Feb 3, 2016

Reader.py class interacts directly with the camera through gphoto2. New
    photos are automatically inserted into a designated directory.
'''
import PhotoUploadConstants as constants
import PhotoUploadUtility as Utility
import time
import os

import subprocess
import re   # regex library
from Queue import Queue

class Reader(object):

    shell = False;

    def __init__(self, orders):
        config = Utility.getProjectConfig()
        self.myOrders = orders
        # Extract relevant config data
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
    
    def run(self):
        print "Hi, I'm a Reader!"

        time.sleep(2) # TEMPORARILY DO NOTHING WHILE INTEGRATING CHANGES
        print "Reader is exiting."
        # Put actual cleanup/saving code here!
        print "Reader successfully exited."
    
def camera_filenames_to_file(outputFileName=None):
    if outputFileName is None:
        raise Exception('camera_filenames_to_file:  missing file name parameter')
    os.system('gphoto2 -L >' + outputFileName)
# RETURNING AN UNKNOWN ERROR -1, NEEDS INVESTIGATION
#    try:
#        outputFileArg = '>' + outputFileName
#        subprocess.check_output(['gphoto2', '-L', outputFileArg]) #shell=False
#    except subprocess.CalledProcessError:
#        print 'Camera is either not connected or not supported'
    
def __getImageNumber(line=None):
    if line is None:
        raise Exception('getImageNumber:  missing line string parameter')
    pattern = '#[0-9]*'     # pound sign followed by any number of digits 0-9
    match = re.search(pattern,line)
    if match:   # match object implicitly true
        return match.group(0)[1:] # first instance of match, stripping the # character
    else:
        return None

def downloadNewImages(fileNameOld=None,fileNameNew=None):
    if fileNameOld is None or fileNameNew is None:
        raise Exception('downloadNewImages:  missing file name parameter')
    # Pythonic diff logic
    f = open(fileNameOld, 'r')
    imageListOld = []
    for line in f:
        imageListOld.append(line)
    f = open(fileNameNew, 'r')
    imageListNew = []
    for line in f:
        imageListNew.append(line)
    diff = set(imageListNew).difference(set(imageListOld)) # those in New not in Old
    # parse diff for valid image numbers
    for line in diff:
        imgNumber = __getImageNumber(line)
        if (imgNumber):
            try:
                # download those images found in diff
                subprocess.check_output(['gphoto2','--get-file', imgNumber])
            except subprocess.CalledProcessError:
                print 'Camera is either not connected or not supported'
                
                