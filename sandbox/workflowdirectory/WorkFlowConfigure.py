'''
Created on Jan 27, 2016

@author: patrickstewart
'''
import ConfigParser
import os.path

class WorkFlowConfigure(object):

    def __init__(self, name=None):
        if name is None:
            raise Exception('Error: no configuration file name specified')
        self.fileName = name
        self.sectionName = 'workflow options'
        self.config = ConfigParser.RawConfigParser()
        if not os.path.isfile(self.fileName):
            print "Config file missing, restoring defaults"
            self.setDefaults().writeConfig()
        else:
            self.config.read(self.fileName)
        
    def writeConfig(self):
        with open(self.fileName, 'wb') as configFile:
            self.config.write(configFile)
            
    def setDefaults(self):
        if not self.config.has_section(self.sectionName):
            self.config.add_section(self.sectionName)
        self.config.set(self.sectionName, 'imageDirectoryName', '/Users/patrickstewart/Coursework/COMP4710/AUPhotoUpload/sandbox/testdirectory/')
        self.config.set(self.sectionName, 'mostRecentCardID', 12345678)
        self.config.set(self.sectionName, 'imageListFileName', 'images.txt')
        return self     # return self to enable chaining
    
    def getConfig(self, option=None):
        if option is None:
            raise Exception("Error: missing parameter for getConfig(option)")
        return self.config.get(self.sectionName, option)
    
    def setConfig(self, option=None, value=None):
        if (option is None) or (value is None):
            raise Exception("Error: missing parameter for setConfig(option)")
        self.config.set(self.sectionName, option, value)
        
        