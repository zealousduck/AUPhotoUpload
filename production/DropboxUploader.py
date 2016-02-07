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
    
    def setUserFile(self, userFileName):
        name = None
        try:
            with open(userFileName) as userFile:
                tempKey = userFile.readline()
                tempSecret = userFile.readline()
                tempToken = userFile.readline()
                self.setApp(tempKey, tempSecret)
                self.setAccessToken(tempToken)
                self.setClient()
                name = self.getClientAccountInfo("display_name")
        except IOError as localError:
            print "Error loading user file. I/O error(%s): %s".format(localError.errno, localError.strerror)
            raise
        return name
            
    
    def setClient(self):
        if self.myAccessToken is not None:
            print "Authenticating account with Dropbox..."
            self.myClient = dropbox.client.DropboxClient(self.myAccessToken)
            self.clientAccountInfo = self.myClient.account_info()
        return None
    
    #User information is stored in a dictionary, as specified in the Dropbox API
    #entries include the following key-value pairs
    #["uid": 12345678, "display_name": "John User", "name_details": {"familiar_name": "John", "given_name": "John", "surname": "User"},
    #"referral_link": "https://www.dropbox.com/referrals/r1a2n3d4m5s6t7", "country": "US",
    #"locale": "en", "email": "john@example.com", "email_verified": false, "is_paired": false,
    #"team": { "name": "Acme Inc.", "team_id": "dbtid:1234abcd" }, "quota_info": { "shared": 253738410565, 
    #"quota": 107374182400000, "normal": 680031877871]
    def getClientAccountInfo(self, jsonKey):
        return self.clientAccountInfo[jsonKey]
    
    
    def uploadFile(self, localName = None, uploadName = None):
        fileSuccess = 0
        try:
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
        except IOError as localError:
            print "Error uploading %s: I/O error(%s): %s" (localName, localError.errno, localError.strerror)
        return fileSuccess
    
    def batchUpload(self, localNames = None, uploadNames = None):
        filesUploaded = 0
        numLocals = len(localNames)
        currentFile = 1
        for localName, uploadName in zip(localNames, uploadNames):
            print "Uploading file %s of %s..." % (currentFile, numLocals),
            fileSuccess = self.uploadFile(localName, uploadName)
            if fileSuccess == 1 :
                print "success."
            
            filesUploaded += fileSuccess
            currentFile += 1
            
        return filesUploaded
    
    def simpleUpload(self, localName = None):
        fileSuccess = self.uploadFile(localName, localName)
        return fileSuccess
        
    def simpleBatch(self, localNames = None):
        filesUploaded = self.batchUpload(localNames, localNames)
        return filesUploaded
    
    def simpleUploadPrompt(self):
        simpleFilename = raw_input("Please input filename: ")
        successfulUpload = self.simpleUpload(simpleFilename)
        if (successfulUpload == 1):
            print "Upload successful."
        return 
    
    def simpleBatchPrompt(self):
        print "For a batch upload, please input the prefix that identifies your files."
        print "For example, to upload img1.jpg img2.jpg and img3.jpg,"
        print "simply enter img1"
        filenamePrefix =  raw_input("Please input your filename prefix: ")
        localFiles = [filename for filename in os.listdir('.') \
            if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)) \
            and filename.startswith(filenamePrefix)]
        numOfFiles = len(localFiles)
        print "%s files found." % (numOfFiles,)
        successfulUploads = self.simpleBatch(localFiles)
        print "%s of %s files successfully uploaded" % (successfulUploads, numOfFiles)
        return
    
    def fetchDefaultUser(self):
        print "No Login information provided, running as default user..."
        defaultUser = ""
        try:
            defaultUser = self.setUserFile("defaultUser.txt")
        except IOError:
            print "Could not load user file. exiting."
            return
        print "Account found for user %s." %(defaultUser)
        return
    
    # The current version expects a .TXT file named defaultUser.txt with 
    # The Key on the first line
    # The Secret on the second line
    # The Access Token on the third line.
    def main(self, interfaceType = None, inputKey = None, inputSecret = None, inputAccessToken = None):
        if interfaceType is None:
            self.fetchDefaultUser()
            userChoice = ""
            userChoices = {"normal" : "Normal: Upload a single file." , \
                    "batch"  : "Batch: Upload a series of files." , \
                    "exit" : "Exit: Exit the program." }    
            while userChoice != "exit":
                print "[MAIN MENU]"
                userChoice = ""
                while (userChoice not in userChoices):
                    for selection in userChoices:
                        print userChoices[selection]
                    userChoice = raw_input("Please select a valid input: ").lower()
                    if userChoice not in userChoices:
                        print "Sorry, your input was not a valid selection."
                        print "[MAIN MENU]"
                if userChoice == "normal":
                    self.simpleUploadPrompt()
                elif userChoice =="batch":
                    self.simpleBatchPrompt()
                elif userChoice == "exit":
                    print "Thank you. Goodbye."
                    return
                else:
                    pass
                print "Returning to menu..."
            
        else:
            pass
        
if __name__ == "__main__": 
    myRunner = DropboxUploader(None, None, None)
    myRunner.main()
    
