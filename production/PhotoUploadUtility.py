'''
Created on Feb 5, 2016

PhotoUploadUtility.py provides a set of utility functions that can be used by
    each of the classes in the project. It also provides constant values for 
    each component to import and use for functionality.
'''

CONFIG_FILE_NAME = 'photoUpload.cfg'
UPLOADS_FILE_NAME = 'imageList.txt'
DEFAULT_CONFIG = 'photoUploadDefaults.cfg'
POLL_TIME = 1   # in seconds
STABLE_INTERNET_COUNT = 5
INACTIVE_COUNT = 30
# OLD_PICS_FILE_NAME = '/home/chris/workspace/AUPhotoUpload/production/oldPics.txt'
# NEW_PICS_FILE_NAME = '/home/chris/workspace/AUPhotoUpload/production/newPics.txt'
OLD_PICS_FILE_NAME = '/home/pi/AUPhotoUpload/production/oldPics.txt' #Place holder for the absolute path for the pi.
NEW_PICS_FILE_NAME = '/home/pi/AUPhotoUpload/production/newPics.txt' #Place holder for the absolute path for the pi.
QMSG_SETTINGS = 10
QMSG_FILE_EXPLORER = 20
QMSG_START = 30
QMSG_SCAN = 40
QMSG_SCAN_DONE = 45
QMSG_SCAN_FAIL = 49
QMSG_HANDLE = 50
QMSG_HANDLE_NONE = 59
QMSG_UPLOAD = 60
QMSG_UPLOAD_USER_FAIL = 64
QMSG_UPLOAD_IMAGE_FAIL = 65
QMSG_UPLOAD_DONE = 69
QMSG_IDLE = 70
QMSG_INTERNET_YES = 90
QMSG_INTERNET_NO = 99

import ConfigParser
import os
import Configurer
import time
import socket

''' 
getProjectConfig() loads the .cfg file into a parseable form. It then
    returns the config object for get() options.
'''
def getProjectConfig():
    config = ConfigParser.RawConfigParser()
    if os.path.isfile(CONFIG_FILE_NAME):
        config.read(CONFIG_FILE_NAME)
    elif os.path.isfile(DEFAULT_CONFIG):
        config.read(DEFAULT_CONFIG)
    else: 
        Configurer.Configurer().revertToDefaults()
    return config


'''
readMessageQueue() handles the race condition problem of reading the
    asynchronous queues.
    Currently the solution is simply to wait a constant amount of time
    to give the queue a 'reasonable' amount of time to update.
'''
def readMessageQueue(queue=None):
    if queue is None:
        raise Exception('readMessageQueue:  missing queue parameter')
    while queue.empty():
        time.sleep(POLL_TIME)
    return queue.get()

'''
checkInternetConnection() allows the application to check the presence
    of an internet connection without utilizing a DNS lookup. By default,
    it utilizes Google's DNS servers, connecting via TCP DNS.
    See: http://stackoverflow.com/questions/3764291/checking-network-connection
'''
def checkInternetConnection(host='8.8.8.8', port=53):
    try:
        socket.setdefaulttimeout(POLL_TIME)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host,port))
        return True
    except Exception as ex:
        print ex
    return False

if __name__ == '__main__':
    getProjectConfig()
