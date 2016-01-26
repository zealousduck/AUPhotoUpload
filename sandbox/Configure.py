'''
Created on Jan 26, 2016

@author: patrickstewart
'''

import ConfigParser

class Configure(object):

    def __init__(self, name=None):
        if name is None:
            self.fileName = 'sampletext.cfg'
        else:
            self.fileName = name
        self.config = ConfigParser.RawConfigParser()
        self.setDefaults()
        self.writeToConfigFile()
            
    def setDefaults(self):
        # determine defaults lol
        # It might be better to have a read-only defaults.cfg file as opposed to hard-coding the values!
        self.config.add_section('Section 1')
        self.config.set('Section 1', 'Option 1', 10)
        self.config.set('Section 1', 'Option 2', 'test')
        
    def writeToConfigFile(self):
        with open(self.fileName, 'wb') as configFile:
            self.config.write(configFile)
        
    # For getting and setting, we can either have individual getters/setters or....
    # we can use identifying fields, like: get('foo') and set('foo', 4)
    # It's a coupling problem
    def getFieldThree(self):
        return self.config.get('Section 1', 'Option 3')
    
    def setFieldThree(self):
        self.config.set('Section 1', 'Option 3', 55.5)
        
# Demonstration code, make sure to refresh your filesystem to see the new .cfg file
cfg = Configure()
cfg.setFieldThree()
cfg.writeToConfigFile()
print cfg.getFieldThree()