'''
    Created on Jan 27, 2016
    Provides functions relating to uploading to dropbox
    @author: Evan Susag
'''
# Note that in order for this to work, you must have the dropbox sdk installed
# if you have pip, the command is simply "pip install dropbox" (may need sudo)
# if not the sdk is available at
# https://www.dropbox.com/developers/downloads/sdks/core/python/dropbox-python-sdk-2.2.0.zip
# after you extract the sdk, the command is simply "python install dropbox"
# Depending on your environment, you may need to include the correct directory in the libraries
# for your project to be able to import dropbox.
# In eclipse, its Window>Preferences>Pydev>Interpreters>Python Interpreter. 
# From here, make sure the python27 interpreter has entries under system PYTHONPATH
# for "python27\lib\site-packages\"
# mine also included "python27\lib\site-packages\dropbox2.2.0-py2.7.egg", but I don't think this is mandatory

import dropbox
import os
class DropboxUploader:
    def __init__(self, inputKey = None, inputSecret  = None, inputAccessToken  = None):
        self.myKey = None
        self.mySecret = None
        self.myClient = None
        self.myAccessToken = None
        self.clientAccountInfo = None
        self.setApp(inputKey, inputSecret)
        self.setAccessToken(inputAccessToken)
        self.setClient()
        return None
    
    def setApp(self, appKey = None, appSecret = None):
        self.myKey = appKey
        self.mySecret = appSecret   
        return None
    
    def setAccessToken(self, inputToken = None):
        self.myAccessToken = inputToken
        return None
    
    def setClient(self):
        if self.myAccessToken is not None:
            self.myClient = dropbox.client.DropboxClient(self.myAccessToken)
            self.clientAccountInfo = self.myClient.account_info()
        return None
    
    def getClientAccountInfo(self, jsonKey):
        return self.clientAccountInfo[jsonKey]
    
    
    def uploadFile(self, localName = None, uploadName = None):
        fileSuccess = 0
        with open(localName, 'rb') as localFile:
            try:
                self.myClient.put_file(str('/' + uploadName), localFile)
                fileSuccess = 1
            except dropbox.rest.ErrorResponse as myError:
                dropResponse = ""
                if myError.status == 400:
                    dropResponse = "Bad Request (http 400)."
                elif myError.status == 507:
                    dropResponse = "User over data quota (http 507)."
                print "Upload failed for local file %s, Dropbox replied with: %s" % (localName, dropResponse)
        return fileSuccess
    
    def batchUpload(self, localNames = None, uploadNames = None):
        filesUploaded = 0
        numLocals = len(localNames)
        currentFile = 1
        for localName, uploadName in zip(localNames, uploadNames):
            print "Uploading file %s of %s." % (currentFile, numLocals)
            fileSuccess = self.uploadFile(localName, uploadName)
            filesUploaded += fileSuccess
            currentFile += 1
            
        return filesUploaded
    
    def simpleUpload(self, localName = None):
        fileSuccess = self.uploadFile(localName, localName)
        return fileSuccess
        
    def simpleBatch(self, localNames = None):
        filesUploaded = self.batchUpload(localNames, localNames)
        return filesUploaded
    
    def setUserFile(self, userFileName):
        with open(userFileName) as userFile:
            tempKey = userFile.readline()
            tempSecret = userFile.readline()
            tempToken = userFile.readline()
            self.setApp(tempKey, tempSecret)
            self.setAccessToken(tempToken)
            self.setClient()
            name = self.getClientAccountInfo("display_name")
            return name
    
    #
    # THE CURRENT VERSION EXPECTS A .TXT file 
    #
    def main(self, interfaceType = None, inputKey = None, inputSecret = None, inputAccessToken = None):
        if interfaceType is None:
            defaultUser = self.setUserFile("defaultUser.txt")
            print "No Login information provided, running as default user " + defaultUser
            normOrBatch = ""
            while (normOrBatch != "Normal" and normOrBatch != "Batch"):
                normOrBatch = raw_input("Normal or Batch upload? ")
            if normOrBatch == "Normal":
                simpleFilename = raw_input("Please input filename: ")
                self.simpleUpload(simpleFilename)
                if (self.simpleUpload(simpleFilename) == 1):
                    print "upload successful"
            else:
                print "For a batch upload, please input the prefix that identifies your files."
                print "For example, to upload img1.jpg img2.jpg and img3.jpg,"
                print "simply enter img1"
                filenamePrefix =  raw_input("Please input your filename prefix: ")
                fileStream = [filename for filename in os.listdir('.') \
                              if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)) \
                            and filename.startswith(filenamePrefix)]
                numOfFiles = len(fileStream)
                print "%s files found." % (numOfFiles,)
                successfulUploads = self.simpleBatch(fileStream)
                print "%s files successfully uploaded" % (successfulUploads)
            
        else:
            pass
if __name__ == "__main__": 
    myRunner = DropboxUploader(None, None, None)
    myRunner.main()
