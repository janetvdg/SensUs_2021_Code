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
from preprocess import preprocess, load_image, analysis, select_ROI_image
from processing.processing_functions import select_ROI
from analysis.Analyse_results_with_connected_components import Measure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') #???TODO

from processing.RunAnalysisHandler import RunAnalysisHandler
from processing.RunROIHandler import RunROIHandler







#ROIs = [[3444, 2316,  480], [1096, 2484,  480], [2348, 1456,  480], [4352,  820,  480]]


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

# 2. SELECTING ROI from last image created in folder /focus
ROI_path = select_ROI_image(DIR_ROI)  # selecting image to select ROI, getting path
print('ROI PATH', ROI_path)
os.chdir(ORIGINAL_FOLDER)  # going back to original working directory
ROIs = select_ROI(ROI_path)
time.sleep(0.1)


# 3. STARTING THE OBSERVER: it will find any new images
# Observer for running the analysis
observer2 = Observer()
event_analysis_handler = RunAnalysisHandler(ROIs, window_size = 5, IMG_FOLDER = IMG_FOLDER) # create event handler
observer2.schedule(event_analysis_handler, path=DIR) # set observer to use created handler in directory
observer2.start()  # creates a new thread
print('TO_LOOK_FOLDER', DIR)




#print('I want this', event_analysis_handler.result())

#TODO: HOW TO GET THE RESULT FROM THERE INSIDE

# sleep until keyboard interrupt, then stop + rejoin the observer
results_list = []

fig = plt.figure()
try:
    while True:
        time.sleep(0.1)  # keeps main thread running
        results_list = event_analysis_handler.get_result()
        print(results_list)
        foreground = [x[1] for x in results_list[1:]]
        print('Foreground', foreground)
        plt.plot(foreground)
        plt.pause(1)
        plt.show()
        plt.clf()

        # TODO: SAVE

except KeyboardInterrupt:  # ctrl-c
    observer2.stop()  # when program stops, it does some work before terminating the thread
    print('last results list', results_list)
    print('observer2 interrupted')
    print('I want this', event_analysis_handler.result)
observer2.join() # is needed to proper end a thread for "it blocks the thread in which you're making the call, until (self.observer) is finished


print('asdf', event_analysis_handler.get_result())


#TODO: ROI
# moving average of the signal result