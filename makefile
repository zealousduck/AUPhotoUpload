photoDir = /home/photos/workspace/AUPhotoUpload/production/_photo_upload_test_directory
pythonDir = /home/photos/workspace/AUPhotoUpload/production

all:
	@echo -e "\nAvailable scripts:\n\tmake stop --> terminate all application components\n\tmake run --> start application in $(photoDir)\n"

stop:
	@echo -e "\nTerminating python and gphoto2 programs\n"
	@killall python && killall sh

run:
	@echo -e "\nLaunching Supervisor and gphoto2\n"
	@cd $(pythonDir) && python Supervisor.py && cd $(photoDir) && gphoto2 --wait-event-and-download

