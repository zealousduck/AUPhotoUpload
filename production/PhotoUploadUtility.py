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
QMSG_SETTINGS = 'msg_settings'
QMSG_START = 'msg_start'
QMSG_FILE_EXPLORER = 'msg_file_explorer'
QMSG_SCAN = 'msg_reader_scan'
QMSG_SCAN_DONE = 'msg_reader_done'
QMSG_HANDLE = 'msg_handler_start'
QMSG_UPLOAD = 'msg_uploader_working'
QMSG_UPLOAD_DONE = 'msg_uploader_done'

import ConfigParser
import os
import Configurer
import time

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


if __name__ == '__main__':
    getProjectConfig()
