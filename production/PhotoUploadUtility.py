'''
Created on Feb 5, 2016

PhotoUploadUtility.py provides a set of utility functions that can be used by
    each of the classes in the project.
'''
import ConfigParser
import os
import PhotoUploadConstants as constants
import Configurer

''' 
getProjectConfig() loads the .cfg file into a parseable form. It then
    returns the config object for get() options.
'''
def getProjectConfig():
    config = ConfigParser.RawConfigParser()
    if os.path.isfile(constants.CONFIG_FILE_NAME):
        config.read(constants.CONFIG_FILE_NAME)
    elif os.path.isfile(constants.DEFAULT_CONFIG):
        config.read(constants.DEFAULT_CONFIG)
    else: 
        Configurer.Configurer().revertToDefaults()
    return config




if __name__ == '__main__':
    getProjectConfig()
