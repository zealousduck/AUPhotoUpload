'''
Created on Feb 3, 2016

Supervisor.py is the parent class and entry point for the PhotoUpload
    application. It creates the child classes that perform the work.
    Direct child processes: Reader, Handler
'''
import PhotoUploadConstants as constants
import Reader
import Handler
from multiprocessing import Process

class Supervisor(object):

    def __init__(self):
        pass
    
    def startReader(self):
        reader = Reader.Reader()
        reader.run()
    
    def startHandler(self):
        handler = Handler.Handler()
        handler.run()
    
    def run(self):
        readerProcess = Process(target = self.startReader)
        readerProcess.start()
        handlerProcess = Process(target = self.startHandler())
        handlerProcess.start()
        readerProcess.join()
        handlerProcess.join()
    
if __name__ == '__main__':
    Supervisor().run()
    
        