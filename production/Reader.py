'''
Created on Feb 3, 2016

Reader.py class interacts directly with the camera through gphoto2. New
    photos are automatically inserted into a designated directory.
'''
import PhotoUploadUtility as Utility
import time
import os
from shutil import copyfile
import subprocess
import re   # regex library
import errno
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
        status = Utility.readMessageQueue(self.myOrders)
        print "READER DEBUG:", status
        try:
            if status == Utility.QMSG_SCAN:
                camera_filenames_to_file(Utility.NEW_PICS_FILE_NAME)
                downloadNewImages(fileNameOld=Utility.OLD_PICS_FILE_NAME, fileNameNew=Utility.NEW_PICS_FILE_NAME)
                os.rename(Utility.NEW_PICS_FILE_NAME, Utility.OLD_PICS_FILE_NAME)
                self.myOrders.put(Utility.QMSG_SCAN_DONE)
        except Exception as e:
            print e
            self.myOrders.put(Utility.QMSG_SCAN_FAIL)
        print "Reader is exiting."
        print "Reader successfully exited."
    
def camera_filenames_to_file(outputFileName=None):
    print "Filenames to file"
    if outputFileName is None:
        raise Exception('camera_filenames_to_file:  missing file name parameter')
    __ensureExists(outputFileName)
    #if not os.path.isfile(outputFileName):
        #open(outputFileName, 'w+').close()
    #__ensureExists(Utility.OLD_PICS_FILE_NAME)
    copyfile(outputFileName, (outputFileName + ".bak"))
    
    with open(outputFileName, 'w+') as outFile:
        try:
            #outputFileArg = '>' + outputFileName
            subprocess.check_call(['gphoto2', '-L'], stdout=outFile) #shell=False
            os.remove(outputFileName + ".bak") # remove the backup file after try
        except subprocess.CalledProcessError:
            print 'Camera is either not connected or not supported' #There is no error in this case. We get the proper outputfile
            copyfile((outputFileName + ".bak"), outputFileName)
            os.remove(outputFileName + ".bak") # remove the backup file after try
            raise Exception('Failed to pull image list from camera')
        outFile.close()
        
def __ensureExists(filename=None):
    if filename is None:
        raise Exception('__ensureExists:  missing filename string parameter.')
    if not os.path.isfile(filename):
        open(filename, 'w+').close()
    
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
    print "download New Images"
    if fileNameOld is None or fileNameNew is None:
        raise Exception('downloadNewImages:  missing file name parameter')
    # Pythonic diff logic
    oldImageSet = set()
    __ensureExists(fileNameOld)
    #if not os.path.isfile(fileNameOld):
        #f = open(fileNameOld, 'w+')
        #f.close()
    f = open(fileNameOld, 'r+')
    for line in f:
        oldImageSet.add(line)
    f.close()
    
    __ensureExists(fileNameNew)
    f = open(fileNameNew, 'r+')
    newImageSet = set()
    for line in f:
        newImageSet.add(line)
    f.close()
    newImageSet.difference_update(oldImageSet) # those in New not in Old
    #diff = set(imageListNew).difference(set(imageListOld)) 
    # parse diff for valid image numbers
    commandArg = ""
    for line in newImageSet:
        imgNumber = __getImageNumber(line)
        if (imgNumber):
            commandArg += imgNumber + ','
    commandArg = commandArg[:-1] #Remove trailing ','
    try:
        # download those images found in diff
        subprocess.check_output(['gphoto2','--get-file', commandArg])
    except subprocess.CalledProcessError:
        print 'Camera is either not connected or not supported'
        raise Exception('Failed to download images from camera')
                
