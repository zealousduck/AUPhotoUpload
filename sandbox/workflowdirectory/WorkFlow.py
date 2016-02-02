'''
Created on Jan 27, 2016

@author: patrickstewart
'''
import WorkFlowConfigure
import WorkFlowHandler

#    Open config file (auto-create if not present?)
configFileName = 'workflow.cfg'
cfg = WorkFlowConfigure.WorkFlowConfigure(configFileName)

#    Pull in relevant configuration data
imageDirectoryName = cfg.getConfig('imageDirectoryName')
mostRecentCardID = cfg.getConfig('mostRecentCardID')
imageListFileName = cfg.getConfig('imageListFileName')

#    Initialize handler
hdlr = WorkFlowHandler.WorkFlowHandler(imageListFileName)

#    Check if fresh memory card

#    If fresh, give handler list of all images currently on, exit

#    Else, pull image list


#    Grab list of image names from camera

#    Perform difference computation

#    Grab list of images themselves by name

#    Upload to Dropbox...???



