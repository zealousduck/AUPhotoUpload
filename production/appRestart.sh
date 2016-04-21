#!/bin/bash
background="&>/dev/null &"
appDir="/home/chris/workspace/AUPhotoUpload/production"

#restart networking
sudo /etc/init.d/network-manager stop #&>/dev/null &
sudo /etc/init.d/network-manager start #&>/dev/null &
#internet reconnects

#force restart gphoto2 incase it is held up
killall gphoto2 &>/dev/null &

#close all python apps. This will close the AUPhotoUplad appDir
killall python &>/dev/null &

#Make a copy of oldPics.txt so the user won't lose newly taken pictures in the upload.
mv oldPics.txt oldPics.txt.bak

#Restart the application
python $appDir/Supervisor.py &>/dev/null &

#Move the original oldPics back. We kill gphoto2 to avoid accidental overwrites of this file. gphoto2 will start back when scan is clicked. 
killall gphoto2
mv oldPics.txt.bak oldPics.txt