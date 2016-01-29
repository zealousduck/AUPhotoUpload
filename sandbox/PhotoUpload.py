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
class DropboxUploader:
    
    def __init__(self, inputKey, inputSecret, inputAccessToken):
        self.myKey = None
        self.mySecret = None
        self.myAccessToken = None
        self.myClient = None
        self.setApp(inputKey, inputSecret)
        self.setAccessToken(inputAccessToken)
        self.setClient()
        return None
    
    def setApp(self, appKey, appSecret):
        self.myKey = appKey
        self.mySecret = appSecret
        return None
    
    def setAccessToken(self, inputToken):
        self.myAccessToken = inputToken
        return None
    
    def setClient(self):
        self.myClient = dropbox.client.DropboxClient(self.myAccessToken)
        print 'linked account: ', self.myClient.account_info()
        return None
    
    def uploadFile(self, localName, uploadName):
        with open(localName, 'rb') as localFile:
            response = self.myClient.put_file(str('/' + uploadName), localFile)
            print 'uploaded: ', response
        return None
    
    def batchUpload(self, localNames, uploadNames):
        for localName, uploadName in zip(localNames, uploadNames):
            self.uploadFile(localName, uploadName)
        return None
    
    def simpleUpload(self, localName):
        self.uploadFile(localName, localName)
        return None
        
    def simpleBatch(self, localNames):
        self.batchUpload(localNames, localNames)
        return None
readKey = ""
readSecret = ""
readToken = ""
readFilename = ""
with open('key.txt', 'r') as keyFile:
    readKey = keyFile.read()
with open('secret.txt', 'r') as secretFile:
    readSecret = secretFile.read()
with open('token.txt', 'r') as tokenFile:
    readToken = tokenFile.read()
with open('photo.txt', 'r') as photoNameFile:
    readFilename = photoNameFile.read()
testUpload = DropboxUploader(readKey, readSecret, readToken)
testUpload.simpleUpload(readFilename)
