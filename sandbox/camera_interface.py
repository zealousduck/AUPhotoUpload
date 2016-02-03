'''
Created on Feb 1, 2016

@author: Chris 
'''
#===============================================================================
# This is an gphoto2 interface that was designed to work through the CLI. It uses
# a combination of linux commands and python This was designed to act as an demo
# and proof of concept. 
#===============================================================================
import os
import sys


#===============================================================================
# This code will be used to allow for verification that camera is seen
#===============================================================================
def check_device():
    os.system('gphoto2 --auto-detect')

# This is code to show all folders on device. The output of this would need reorganizing to be useful 
def list_Folders():
    os.system('gphoto2 -l')

# This shows all the files on a device. The output of this would need reorganizing to be useful       
def list_Pictures():
    os.system('gphoto2 -L')

# Transfers the image of a specific file
def transfer_Specific():
    print('If you do not Know the number of photo you want, then run the list photos menu option')
    picNum = raw_input('Enter the number of the picture you wont to Transfer: ')
    os.system('cd ~/Pictures/meta_new/ && gphoto2 --get-metadata=' + str(picNum) + ' --skip-existing')
    redundancy_checker()
    os.system('cd ~/Pictures/ && gphoto2 -p ' + str(picNum) + ' --skip-existing')
    
# Transfers a range of images    
def tranfer_Range():
    print('If you do not Know the range of photos you want, then run the list photos menu option')
    range1 = raw_input('Enter the first number in the range you want to transfer: ')
    range2 = raw_input('Enter the second number in the range you want to transfer: ')
    os.system('cd ~/Pictures/meta_new/ && gphoto2 --get-metadata=' + str(range1) + '-' + str(range2) + ' --skip-existing')
    redundancy_checker()
    os.system('cd ~/Pictures/photos && gphoto2 -p ' + str(range1) + '-' + str(range2) + ' --skip-existing')

# Code to transfer all pictures on the device
def transfer_ALL():
    os.system('rm ~/Pictures/new_new/*') # Make sure old "new" images arn't staying around
    os.system('cd ~/Pictures/meta_new/ && gphoto2 --get-all-metadata --skip-existing --quiet')
    redundancy_checker()
    os.system('cd ~/Pictures/photos && gphoto2 -P --skip-existing')
    
# This will wait for any captured picture and download it to the pi.
def transfer_Captured():
    # This method still needs a way to turn off transfer
    # Could use killall gphoto2 to end session
    print('All images captured will be transfered')
    print('To exit, Press "Ctrl+C." You will need to restart the application.')
    os.system('gphoto2 --wait-event-and-download')

#===============================================================================
# This Function handles errors. It currently handles restarting gphoto2 if it is 
# busy and unusable. It works by calling the killall command. If gphoto2 is not 
# busy then nothing happens but if it is busy, then it is restarted. The command
# runs without output
#===============================================================================
def error_handler():    
    os.system('killall -q gphoto2')

# Rudimentary redundancy checker using meta data and diff
def redundancy_checker():
    redundancy = True
    # Write information about what files are different and what files are new
    os.system('cd ~/Pictures/ && diff meta_new meta > logs/metadiff.txt')
    os.system('ls ~/Pictures/meta_new > ~/Pictures/logs/metaNew.txt')
    
    # Counts the number of different files and new files and writes the numbers to txt files
    os.system('sed -n \'$=\' ~/Pictures/logs/metadiff.txt > ~/Pictures/logs/numDiff.txt')
    os.system('sed -n \'$=\' ~/Pictures/logs/metaNew.txt > ~/Pictures/logs/numNew.txt')
    
    # Find number of differences in both desired files
    with open("/home/chris/Pictures/logs/numDiff.txt") as diff:
        diffNum = diff.readline()
        diff.close()
    with open("/home/chris/Pictures/logs/numNew.txt") as new:
        newNum = new.readline()
        new.close()
    
    # If there are no redundancies
    if newNum == diffNum:
        redundancy = False
        
    # If there are redundancies
    # In this case we refer to diffNum.txt to figure out what to upload    
    if newNum != diffNum:
        redundancy = True
        
    #return redundancy
    os.system('mv -u ~/Pictures/meta_new/* ~/Pictures/meta/ ') #copy the new meta data into the rest for archiving
    os.system('ls ~/Pictures/meta > ~/Pictures/logs/meta_Manifest') # A manifest of all uploaded files
    return redundancy
    

def cli_interface():
    print('Menu: \n')
    print('\t 1) Check Device connection.')
    print('\t 2) List all folders on device.')
    print('\t 3) List all pictures on device. ')
    print('\t 4) Transfer Picture from specific.')
    print('\t 5) Transfer Pictures from a range.')
    print('\t 6) Transfer all pictures on Device.')
    print('\t 7) Transfer all pictures being captured.')
    print('\t 8) Manually restart gphoto2. Use in case gphoto2 is hung up.')
    print('\t 9) Exit out of the program. \n')
    option = int(input('Choose one of the above options: '))
    # Removed all recursive calls in if statements to reduce the number of recursive calls to one 
    if option == 1:
        error_handler()
        check_device()
    if option == 2:
        error_handler()
        list_Folders()
    if option == 3:
        error_handler()
        list_Pictures()
    if option == 4:
        error_handler()
        transfer_Specific()
    if option == 5:
        error_handler()
        tranfer_Range()
    if option == 6:
        error_handler()
        transfer_ALL()
    if option == 7:
        error_handler()
        transfer_Captured()
    if option == 8:
        print('Manually restarted gphoto2')
        error_handler()
    if option == 9:
        print('Program is exiting...') 
        sys.exit()
         
    if option < 1 and option > 9:
        print('You entered an invalid option. Select again')
    
    #wait for user to finish reading output
    raw_input('\n Press enter to continue back to main menu. \n')   #Remove raw for python 3
    # Restart the CLI to allow for another option to be picked
    cli_interface()
    
#===============================================================================
#This is where all the main code is run 
#===============================================================================
cli_interface();
#redundancy_checker()
