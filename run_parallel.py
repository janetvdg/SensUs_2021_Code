#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run parallel

Created on Fri Aug 27 11:11:05 2021

@author: janet
"""
             
import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
import os
from preprocess import preprocess, load_image, analysis
from processing.processing_functions import select_ROI
from analysis.Analyse_results_with_connected_components import Measure

from processing.RunAnalysisHandler import RunAnalysisHandler
from processing.RunROIHandler import RunROIHandler







ROIs = [[3444, 2316,  480],
 [1096, 2484,  480],
 [2348, 1456,  480],
 [4352,  820,  480]]


## 1. DESCRIBING FOLDERS
ORIGINAL_FOLDER = os.path.dirname(os.path.realpath(__file__))
print('THIS IS ORIGINAL FOLDER PATH', str(ORIGINAL_FOLDER))
IMG_FOLDER = os.path.abspath('images') #Folder where the images taken by the camera to be processed will be located
IMG_PROCESSED_FOLDER = os.path.abspath('images_processed')  #Folder where the resulting images will be located
DIR_ROI = os.path.abspath('focus')
path = IMG_FOLDER
os.chdir(path)
dirs = sorted(filter(os.path.isdir, os.listdir(path)), key=os.path.getctime)
os.chdir(ORIGINAL_FOLDER)

DIR = os.path.join(IMG_FOLDER, dirs[-1]) # folder to look at

# moving average of the signal result



# 2. STARTING THE OBSERVER: it will find any new images
# Observer for selecting ROI
#observer1 = Observer()
#event_ROI_handler = RunROIHandler() # create event handler
#observer1.schedule(event_ROI_handler, path=DIR_ROI) # set observer to use created handler in directory
#observer1.start()
#print('path DIR ROI', DIR_ROI)

# sleep until keyboard interrupt, then stop + rejoin the observer
#try:
#    while True:
#        time.sleep(1)
#except KeyboardInterrupt:  #ctrl-C
#    print('observer1 interrupted')
#    observer1.stop()

#observer1.join()  # it makes the caller wait until the thread terminates


# Observer for running the analysis
observer2 = Observer()
event_analysis_handler = RunAnalysisHandler(ROIs, window_size = 5, IMG_FOLDER = IMG_FOLDER) # create event handler
observer2.schedule(event_analysis_handler, path=DIR) # set observer to use created handler in directory
observer2.start()  # creates a new thread
print('TO_LOOK_FOLDER', DIR)

#TODO: HOW TO GET THE RESULT FROM THERE INSIDE

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)  # keeps main thread running
except KeyboardInterrupt:  # ctrl-c
    observer2.stop()  # when program stops, it does some work before terminating the thread
    print('observer2 interrupted')
    print('result', result)
observer2.join() # is needed to proper end a thread for "it blocks the thread in which you're making the call, until (self.observer) is finished




#TODO: ROI