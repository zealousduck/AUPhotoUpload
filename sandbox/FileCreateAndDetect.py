'''
Created on Jan 20, 2016

@author: patrickstewart
'''

import os
import time

def fileCreator():
    nameFormat = 'IMG_0'
    
    for imageNumber in range(0,10):
        f = open((nameFormat + str(imageNumber)), 'w+')
        f.close()
#         time.sleep(1)
    
def directoryPrinter():
    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            print(os.path.join(dirname, filename))
        
# Demonstration code   
directory = 'testdirectory'
os.chdir(directory)
fileCreator()
directoryPrinter()
