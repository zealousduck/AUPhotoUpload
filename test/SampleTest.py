'''
Created on Feb 13, 2016

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
    output = ('test_01\n'
              '\t1. Run the test\n'
              '\t2. Check if it passes\n')
    print output
    result, passed = isPassed()
    output += passed
    return (result, output)

def test_02():
    output = ('test_01\n'
              '\t1. Run the test\n'
              '\t2. Check if it passes\n')
    print output
    result, passed = isPassed()
    output += passed
    return (result, output)

if __name__ == '__main__':
    Tester.run('SampleTest')
    
    
