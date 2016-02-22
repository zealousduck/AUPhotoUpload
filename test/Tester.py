'''
Created on Feb 12, 2016

@author: patrickstewart


'''

import os
import datetime
import SampleTest 
import ReaderTest

def generateFileName(testName=None):
    i = str(datetime.datetime.now())
    # Convert '2016-02-08 11:16:04.123456 format to nicer filename
    fileName = testName + '-' + i[0:10] + '-' + i[11:13] + '-' + i[14:16] + '-' + i[17:19] + '.log'
    return fileName

def getTesterName():
    testerName = raw_input('Name of Tester: ')
    return testerName

def getTests(name=None):
    if name is None:
        availableTests = ['0. SampleTest', '1. ReaderTest']
        for testName in availableTests:
            print testName
        testName = raw_input('Name of Tests File: ')
    else:
        testName = name
    testName = testName.lower()
    
    testList = None
    if testName == 'sampletest' or testName[0:1] == '0':
        testList = SampleTest.getTestList()
        testName = 'sampletest'
    elif testName == 'readertest' or testName[0:1] == '1':
        testList = ReaderTest.getTestList()
        testName = 'readertest'
    elif testName == 'handlertest' or testName[0:1] == '2':
        #testList = SampleTest.getTestList()
        print 'Unimplemented tests!'
    elif testName == 'uploadertest' or testName[0:1] == '3':
        #testList = SampleTest.getTestList()
        print 'Unimplemented tests!'
    elif testName == 'configurertest' or testName[0:1] == '4':
        #testList = SampleTest.getTestList()
        print 'Unimplemented tests!'
    if testList is None:
        raise Exception('Invalid tests name: ' + testName)
    
    return testName, testList

def run(testNameIn=None):
    if not os.path.isdir('testlogs'):
        os.mkdir('testlogs')
    os.chdir('testlogs')
    testerName = getTesterName()
    testName, testList = getTests(testNameIn)
    fileName = generateFileName(testName)
    logFile = open(fileName, 'w+')
    logFile.write('Name of Tester: ' + testerName + '\n')
    logFile.write('Name of Tests: ' + testName + '\n')
    logFile.write('Time of Tests: ' + str(datetime.datetime.now()) + '\n')
    overallScore = 0
    for test in testList:
        passScore, outputString = test()
        logFile.write(outputString)
        overallScore += passScore
    
    testsPassedMsg = 'Passed ' + str(overallScore) + ' tests out of ' + str(len(testList))
    print testsPassedMsg
    logFile.write(testsPassedMsg)
    print 'Results written out to', fileName
    logFile.close()
    
if __name__ == '__main__':
    run()
        
