'''
Created on Jan 27, 2016

@author: patrickstewart
'''

class WorkFlowHandler(object):

    def __init__(self, name=None):
        if name is None:
            raise Exception('Error: no image list file name specified')
        self.imageList = []
        self.fileName = name
        try:
            f = open(self.fileName, 'r+')
            for line in f:
                self.imageList.append(line)
            f.close()
        except:
            print("Error: failed to open file: " + self.fileName)
    
    def emptyList(self):
        self.imageList = []
        open(self.fileName, 'w').close()    # overwrites to blank file and immediately closes
        
    def updateList(self, newList):
        # check that each element is a string?? maybe not necessary for getDifference() code...
        self.imageList = list(newList) # copy data, not just reference
        f = open(self.fileName, 'w+')
        for element in self.imageList:
            f.write(element)
        f.close()
        
    def getDifference(self, newList):
        differenceList = []
        for element in newList:
            if (element not in self.imageList): # verify correctness for strings!!!
                differenceList.append(element)
        return differenceList