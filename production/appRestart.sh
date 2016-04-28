#!/bin/bash

#force restart gphoto2 incase it is held up
killall gphoto2 #&>/dev/null &

#close all python apps. This will close the AUPhotoUplad appDir
killall python #&>/dev/null &

#Restart the application
python /home/pi/AUPhotoUpload/production/Supervisor.py & #&>/dev/null &
