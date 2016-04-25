'''
Created on Feb 3, 2016

Uploader.py class uploads queued images to Dropbox with its API.
'''
import PhotoUploadUtility as Utility
import multiprocessing
import os
import time
import dropbox
from multiprocessing import Process, Queue
from Queue import Empty

class UploadWorker(Process):
    def __init__(self, workQueue,failQueue, inMyClient):
        super(UploadWorker, self).__init__()
        self.queue = workQueue
        self.errorQueue = failQueue
        self.localName = None
        self.myClient = inMyClient
        
    def run(self):
        print "Worker started."
        data = self.dequeue()
        while data is not None:
            self.localName = data
            self.peonUpload()
            data = self.dequeue()
        print "Worker exiting..."
        
    def dequeue(self):
        return self.queue.get()
    
    def peonUpload(self):
        if self.localName is None:
            return
        print "uploading " +  self.localName
        try:
            with open(self.localName, 'rb') as localFile:
                try:
                    self.myClient.put_file(str('/' + self.localName), localFile)
                except dropbox.rest.ErrorResponse as myError:
                    dropResponse = "Unknown Error"
                    if myError.status == 400:
                        dropResponse = "Bad Request (http 400)."
                    elif myError.status == 507:
                        dropResponse = "User over data quota (http 507)."
                    print "Upload failed for local file " + self.localName + ", Dropbox replied with: " + dropResponse
                    self.errorQueue.put(self.localName)
        except IOError as localError:
            print "Error uploading " + self.localName + ": I/O error(" + str(localError.errno) + "): " + localError.strerror
            self.errorQueue.put(self.localName)
        print "upload complete for", self.localName

class Uploader(object):
    def __init__(self, q=None, orderQueue = None):
        if q is None:
            raise Exception('Uploader.__init__():  missing parameter')
        if not isinstance(q, multiprocessing.queues.Queue):
            raise Exception('Uploader.__init__():  parameter not of type ""')
    
        self.queue = q
        self.orders = orderQueue
        config = Utility.getProjectConfig()
        # Extract relevant config data
        inputKey = config.get("dropboxinfo", "key")
        inputSecret = config.get("dropboxinfo", "secret")
        inputAccessToken = config.get("dropboxinfo", "accesstoken")
        self.directoryName = config.get('directories', 'imagedirectory')
        os.chdir(self.directoryName)
        # INSERT DROPBOX DATA FROM CONFIG HERE
        self.myKey = inputKey
        self.mySecret = inputSecret
        self.myAccessToken = inputAccessToken
        self.myClient = None
        self.clientAccountInfo = None
        self.setApp(inputKey, inputSecret)
        self.setAccessToken(inputAccessToken)
        
    def run(self):
        print "Hi, I'm an Uploader!"
        print "Uploader, checking in! pid:", os.getpid()
        response = 0
        status = Utility.readMessageQueue(self.orders)
        if self.clientSucess():
            if status == Utility.QMSG_UPLOAD:
                self.uploadBatch()
            time.sleep(1)
            if self.queue.empty():
                response = Utility.QMSG_UPLOAD_DONE
            else:
                response = Utility.QMSG_UPLOAD_IMAGE_FAIL
            
        else:
            response = Utility.QMSG_UPLOAD_USER_FAIL
            #print "12 rare pepes found."
        # tell Handler we're done
        self.orders.put(response)
        print "Uploader is exiting."
    
    def clientSucess(self):
        theCase = False
        try:
            self.setClient()
            theCase = True
        except:
            theCase = False
        finally:
            return theCase
    
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
    
    
    #User information is stored in a dictionary, as specified in the Dropbox API
    #entries include the following key-value pairs
    #["uid": 12345678, "display_name": "John User", "name_details": {"familiar_name": "John", "given_name": "John", "surname": "User"},
    #"referral_link": "https://www.dropbox.com/referrals/r1a2n3d4m5s6t7", "country": "US",
    #"locale": "en", "email": "john@example.com", "email_verified": false, "is_paired": false,
    #"team": { "name": "Acme Inc.", "team_id": "dbtid:1234abcd" }, "quota_info": { "shared": 253738410565, 
    #"quota": 107374182400000, "normal": 680031877871]
    def getClientAccountInfo(self, jsonKey):
        return self.clientAccountInfo[jsonKey]
    
    def dequeue(self):
        requiredItem = None
        try:
            requiredItem = self.queue.get_nowait()
        except Empty:
            requiredItem = None 
        return requiredItem
    
    def uploadFile(self, localName = None):
        if localName is None:
            return
        print "uploading ", localName
        try:
            with open(localName, 'rb') as localFile:
                try:
                    self.myClient.put_file(str('/' + localName), localFile)
                except dropbox.rest.ErrorResponse as myError:
                    print "Upload failed for local file %s, Dropbox replied with: %s" % (localName, myError.body)
        except IOError as localError:
            print "Error uploading %s: I/O error(%s): %s" % (localName, localError.errno, localError.strerror)
    
    def uploadBatch(self):
        workerStorage = []
        totalWorkers = 3
        numWorkers = 0
        numUploads = 0
        time.sleep(1)
        if not self.queue.empty():
            managedQueue = Queue()
            failQueue = Queue()
            while not self.queue.empty():
                managedQueue.put(self.queue.get())
                numUploads += 1
                time.sleep(1)
            print "Starting Batch of " + str(numUploads) + " images."
            for workerCount in range(totalWorkers):
                managedQueue.put(None)
            for workerCount in range(totalWorkers):
                workerStorage.append(UploadWorker(managedQueue,failQueue,self.myClient))
                numWorkers += 1
            for worker in workerStorage:
                worker.start()
            print str(numWorkers) + " workers started." 
            time.sleep(Utility.POLL_TIME) 
            print "Waiting for uploads to finish..."
            for worker in workerStorage:
                worker.join()
            while not managedQueue.empty():
                time.sleep(Utility.POLL_TIME)
            print str(numWorkers) + " workers ended."
            time.sleep(1)
            while not failQueue.empty():
                self.queue.put(failQueue.get())
            print "Batch Upload finished..."
        else:
            print "Queue currently empty, canceling upload."
            
