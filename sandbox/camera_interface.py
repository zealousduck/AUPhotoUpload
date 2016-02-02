'''
Created on Feb 1, 2016

@author: Chris 
'''
#===============================================================================
# This code is going to serve as the interface between the raspberry pi and the camera.
# This code currently used command line but should be expanded to a GUI
# 
#===============================================================================
import os


#===============================================================================
# This code will be used to allow for verification that camera is seen
#===============================================================================
def check_device():
    os.system('gphoto2 --auto-detect')
    
def list_Pictures():
    # This function needs to be expanded to receiving only img number and image name.
    # Needs to have all other 'Useless' out removed
    # Change to allow only images of certain types to be shown
    # For Gui Interface needs to receive thumbnails
    os.system('gphoto2 -L')

def transfer_Specific():
    print('If you do not Know the number of photo you want, then run the list photos menu option')
    picNum = input('Enter the number of the picture you wont to Transfer: ')
    os.system('cd ~/Pictures/ && gphoto2 -p ' + picNum + ' --skip-existing')
    
def tranfer_Range():
    print('If you do not Know the range of photos you want, then run the list photos menu option')
    range1 = input('Enter the first number in the range you want to transfer')
    range2 = input('Enter the second number in the range you want to transfer')
    os.system('cd ~/Pictures/ && gphoto2 -p ' + range1 + '-' + range2 + ' --skip-existing')

def transfer_ALL():
    # Below line needs to be changed to proper directory before production
    os.system('cd ~/Pictures/ && gphoto2 -P --skip-existing')
    #os.system('gphoto2 -P --skip-existing')     #--skip-existing handles duplicate checking
    
def transfer_Captured():
    # This method still needs a way to turn off transfer
    # Could use killall gphoto2 to end session
    print('All images captured will be transfered')
    os.system('gphoto2 --wait-event-and-download')

#===============================================================================
# If gphoto2 returns an error. Then the system needs to handle it
# This function will detect if gphoto2 is connecting with the camera when it is supposed to be disconnected
# Then it will run killall on gphoto2 to release it
# This function can be used to manually restart gphoto also
#===============================================================================
def error_handler():
    # Handles errors with gphoto2 not being properly killed
    # Still needs a way to check if gphoto2 is being held up by another process
    print('error occured')
    os.system('killall gphoto2') #This will end any 
    
def cli_interface():
    print('Menu: \n')
    print('\t 1) Check Device connection.')
    print('\t 2) List all pictures on device. ')
    print('\t 3) Transfer Picture from specific.')
    print('\t 4) Transfer Pictures from a range.')
    print('\t 5) Transfer all pictures on Device.')
    print('\t 6) Transfer all pictures being captured. \n')
    option = int(input('Choose one of the above options: '))
    if option == 1:
        check_device()
        cli_interface()
    if option == 2:
        list_Pictures()
        cli_interface()
    if option == 3:
        transfer_Specific()
        cli_interface()
    if option == 4:
        tranfer_Range()
        cli_interface()
    if option == 5:
        transfer_ALL()
        cli_interface()
    if option == 6:
        transfer_Captured()
        cli_interface()
    else:
        print('\n You selected an invalid option. Select again \n')
        cli_interface();
    
#===============================================================================
#This is where all the main code is run 
#===============================================================================
cli_interface();
