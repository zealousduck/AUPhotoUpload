'''
Created on Feb 16, 2016

@author: patrickstewart
'''

import Tester

def getTestList():
    # Return each test by name
    testList = [test_01, test_02]
    return testList

def isPassed():
    outcome = raw_input('PASS? ')
    if outcome.upper() == 'PASS':
        result = 1
    else:
        result = 0
    output = 'Result: '
    if result == 1:
        output += 'PASS\n'
    else:
        output += 'FAIL\n'
    return result, output

def test_01():
    testName = 'Camera Connection'
    output = (testName + '\n'
              '\t1. Connect the camera via USB\n'
              '\t2. Verify log includes "Camera Connected!" message\n'
              '\t3. Disconnect the camera\n'
              '\t4. Verify log includes "Camera Disconnected!" message\n')
    print output
    result, passed = isPassed()
    output += passed
    return (result, output)

def test_02():
    testName = 'Downloaded Images stay on Camera'
    output = (testName + '\n'
              '\t1. Connect the camera via USB\n'
              '\t2. Open up the directory specified in the config file\n'
              '\t3. Take a new photo\n'
              '\t4. Verify photo appears in specified directory\n'
              '\t5. Open up the directory the filesystem gives the camera\n'
              '\t6. Verify photo appears in camera memory\n')
    print output
    result, passed = isPassed()
    output += passed
    return (result, output)

if __name__ == '__main__':
    Tester.run('ReaderTest')
    
