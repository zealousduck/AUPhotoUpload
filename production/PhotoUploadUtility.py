'''
Created on Feb 5, 2016

PhotoUploadUtility.py provides a set of utility functions that can be used by
    each of the classes in the project. It also provides constant values for 
    each component to import and use for functionality.
'''

CONFIG_FILE_NAME = 'photoUpload.cfg'
DEFAULT_CONFIG = 'photoUploadDefaults.cfg'
POLL_TIME = 3   # in seconds

import ConfigParser
import os
import Configurer

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


if __name__ == '__main__':
    getProjectConfig()
