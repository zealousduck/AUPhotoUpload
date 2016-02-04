'''
Created on Feb 3, 2016

Configurer.py class operates on the designated configuration file to adjust
    the values via a script (instead of accessing via a text editor). Ideally,
    Configurer will plug into a GUI to provide a user-friendly configuration.
'''
import PhotoUploadConstants as constants
import ConfigParser
from shutil import copyfile

class Configurer(object):

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        pass
    
    def getOption(self, section=None, option=None):
        pass
    
    def setOption(self, section=None, option=None, value=None):
        return self     # return self to allow call chaining
    
    def revertToDefaults(self):
        # copyfile completely replaces the old file
        copyfile(constants.DEFAULT_CONFIG, constants.CONFIG_FILE_NAME)
    
    def saveSettings(self):
        with open(self.fileName, 'wb') as configFile:
            self.config.write(configFile)
            
if __name__ == '__main__':
    Configurer().revertToDefaults()
    print constants.CONFIG_FILE_NAME, "reverted to default values"
    