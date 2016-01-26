'''
Created on Jan 25, 2016

@author: patrickstewart
'''

import os

class DirectoryLister(object):

    def __init__(self):
        self.CURRENT_DIRECTORY = '.'
    
    def getDirectoryList(self, directoryName=None):
        if (directoryName is None):
            return None
        
        directoryList = []
        for directoryName, directoryNames, fileNames in os.walk(directoryName):
            for fileName in fileNames:
                directoryList.append(fileName)
        return directoryList
        
lister = DirectoryLister()
print(lister.getDirectoryList())
print(lister.getDirectoryList(lister.CURRENT_DIRECTORY))
print(lister.getDirectoryList('testdirectory'))        
