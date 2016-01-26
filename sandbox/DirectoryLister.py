'''
Created on Jan 25, 2016

@author: patrickstewart
'''

import os

class DirectoryLister(object):

    def __init__(self):
        self.CURRENT_DIRECTORY = '.'
    
    def getDirectoryList(self, path=None):
        if (path is None):
            return None
        
        # Shallow solution
        directoryList = []
        for item in os.listdir(path):
            directoryList.append(item)
                       
#         # Recursive solution
#         for directoryName, directoryNames, fileNames in os.walk(path):
#             for fileName in fileNames:
#                 # directoryList.append(os.path.join(path, fileName))
#                 directoryList.append(fileName)

        return directoryList
        
        
# Demonstration code   
lister = DirectoryLister()
print(lister.getDirectoryList())
print(lister.getDirectoryList(lister.CURRENT_DIRECTORY))
print(lister.getDirectoryList('testdirectory'))  
print(lister.getDirectoryList('/Volumes'))        
