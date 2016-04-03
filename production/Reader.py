'''
Created on Feb 3, 2016

Reader.py class interacts directly with the camera through gphoto2. New
    photos are automatically inserted into a designated directory.
'''
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
        status = Utility.readMessageQueue(self.myOrders)
        if status == Utility.QMSG_SCAN:
            camera_filenames_to_file(Utility.NEW_PICS_FILE_NAME)
            downloadNewImages(fileNameOld=Utility.OLD_PICS_FILE_NAME, fileNameNew=Utility.NEW_PICS_FILE_NAME)
            os.rename(Utility.NEW_PICS_FILE_NAME, Utility.OLD_PICS_FILE_NAME)
        print "Reader is exiting."
        # Put actual cleanup/saving code here!
        print "Reader successfully exited."
    
def camera_filenames_to_file(outputFileName=None):
    if outputFileName is None:
        raise Exception('camera_filenames_to_file:  missing file name parameter')
    if not os.path.isfile(outputFileName):
        open(outputFileName, 'w+')
    with open(outputFileName, 'w+') as outFile:
        try:
            #outputFileArg = '>' + outputFileName
            subprocess.check_call(['gphoto2', '-L'], stdout=outFile) #shell=False
        except subprocess.CalledProcessError:
            print 'Camera is either not connected or not supported' #There is no error in this case. We get the proper outputfile

    outFile.close()
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
    f = open(fileNameOld, 'r+')
    imageListOld = []
    for line in f:
        imageListOld.append(line)
    f.close()
    f = open(fileNameNew, 'r+')
    imageListNew = []
    for line in f:
        imageListNew.append(line)
    f.close()
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
                

# if __name__ == '__main__':
#     nFile = "newPics"
#     oFile = "oldPics"
#     camera_filenames_to_file(oFile)     #Runs whenever supervisor is launched
    #Waits for new pictures to be taken
#     camera_filenames_to_file(nFile) #Runs whenever button click for upload photo is launched.
#     downloadNewImages(oFile,nFile) #We will probably need to point this to the proper directory later on
    