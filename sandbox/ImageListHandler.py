'''
Created on Jan 25, 2016

@author: patrickstewart

ImageListHandler.py is a prototype class designed to provide operations on
a list of image names.
'''

class ImageListHandler(object):

    def __init__(self):
        self.imageList = []
    
    def emptyList(self):
        # might need to free memory due to constraints?
        self.imageList = []
        
    def updateList(self, newList):
        # check that each element is a string?? maybe not necessary for getDifference() code...
        self.imageList = list(newList) # copy data, not just reference
        
    def getDifference(self, newList):
        differenceList = []
        for element in newList:
            if (element not in self.imageList): # verify correctness for strings!!!
                differenceList.append(element)
        return differenceList
    
handler = ImageListHandler()
C = ['IMG_001', 'IMG_002', 'IMG_003']
D = ['IMG_001', 'IMG_002', 'IMG_003', 'IMG_004', 'IMG_005']
handler.updateList(C)
print(handler.getDifference(D))
handler.emptyList()
print(handler.getDifference(D))
    
    
        