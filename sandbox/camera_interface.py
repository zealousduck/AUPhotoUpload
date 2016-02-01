'''
Created on Feb 1, 2016

@author: chris
'''

import os


def check_device():
    os.system('gphoto2 --auto-detect')
    cli_interface()
    
def list_Pictures():
    # This function needs to be expanded to receiving only img number and image name.
    # Needs to have all other 'Useless' out removed
    # Change to allow only images of certain types to be shown
    # For Gui Interface needs to receive thumbnails
    os.system('gphoto2 -L')

def transfer_Specific():
    print('Input the image number of the picture you would like to transfer')
    print('If you do not know your picture number, then run list picture')
    

def transfer_ALL():
    os.system('gphoto2 -P')
    
def cli_interface():
    print('Menu: \n')
    print('\t 1) Check Device connection.')
    print('\t 2) List all pictures on device. ')
    print('\t 3) Transfer Picture from range.')
    print('\t 4) Transfer all pictures on Device.')
    print('\t 5) Transfer all pictures being captured. \n')
    option = int(input('Choose one of the above options: '))
    if option == 1:
        check_device()
    if option == 2:
        list_Pictures()
    else:
        print('You selected an invalid option. Select again')
        cli_interface();
    

cli_interface();

