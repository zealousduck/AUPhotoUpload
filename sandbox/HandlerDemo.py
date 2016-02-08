'''
Created on Feb 7, 2016

@author: patrickstewart
'''
import os

class HandlerDemo(object):

    def __init__(self):
        pass
    
    def getDirectoryList(self, path=None):
        if (path is None):
            return None
        directoryList = []
        for item in os.listdir(path):
            directoryList.append(item)
        return directoryList
    
    def getListDifference(self, oldList, newList):
        differenceList = []
        for element in newList:
            if (element not in oldList): # verify correctness for strings!!!
                differenceList.append(element)
        return differenceList
        
        
if __name__ == '__main__':
    demo = HandlerDemo()
    try:
        os.chdir('testdirectory')
        os.system('rm IMG_*')   # Clean up directory
    except:
        os.makedirs('testdirectory')
    try:
        input('Continue...')
    except:
        pass
    # Populate with "old" images
    for i in range(0,5):
        os.system('touch IMG_0' + str(i))   
    oldImages = demo.getDirectoryList('.')  # Current directory
    print 'Images in directory:', oldImages
    try:
        input('Continue...')
    except:
        pass
    for i in range(5,10):
        os.system('touch IMG_0' + str(i))
    newImages = demo.getDirectoryList('.')
    print 'Images in directory:', newImages
    print 'Difference:', (demo.getListDifference(oldImages, newImages))
    
        
    
        
    