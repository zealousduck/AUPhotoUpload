'''
Created on Feb 3, 2016

Configurer.py class operates on the designated configuration file to adjust
    the values via a script (instead of accessing via a text editor). Ideally,
    Configurer will plug into a GUI to provide a user-friendly configuration.
'''
import PhotoUploadUtility as Utility
import ConfigParser
import os.path
from shutil import copyfile

class Configurer(object):

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.fileName = 'photoUpload.cfg'
        pass
    
    def getOption(self, section=None, option=None):
        pass
    
    def setOption(self, section=None, option=None, value=None):
        return self     # return self to allow call chaining
    
    def revertToDefaults(self):
        if not os.path.isfile(Utility.DEFAULT_CONFIG):
            self.config.add_section('directories')
            self.config.add_section('dropboxinfo')
            self.config.add_section('carddata')
            self.config.set('directories', 'imagedirectory', '.')   # current
            self.config.set('dropboxinfo', 'key', 'kpwogxeclcczgmf')
            self.config.set('dropboxinfo', 'secret', 'tq1fl93eraqbh97')
            self.config.set('dropboxinfo', 'accesstoken', 'n0d7CWbJI0AAAAAAAAAACHuj83rJmyPJsFveoeZore8O7xctu8NfaC0EwnEiWB7I')
            self.config.set('carddata', 'recentcardid', 00000000)
            self.saveSettings('photoUploadDefaults.cfg')
        # copyfile completely replaces the old file
        copyfile(Utility.DEFAULT_CONFIG, Utility.CONFIG_FILE_NAME)
            
    def saveSettings(self, name=None):
        if name is None:
            raise Exception('Configurer.saveSettings():  missing parameter')
        with open(name, 'wb') as configFile:
            self.config.write(configFile)
            configFile.close()
            
if __name__ == '__main__':
    Configurer().revertToDefaults()
    print Utility.CONFIG_FILE_NAME, "reverted to default values"
    