#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run parallel

This file detects the creation of a new file in a folder, which is then uploaded.
It will run in parallel with the creation of these files, stacking them in the size of a window, running the preprocessing
of the images and analysing them in order to get a result in the form of percentage of pixels detected, that correspond
to an estimation of the number of AU-NP detected by the SenSwiss sensor 2021, based on SPR in AU-NHA.

Created on Fri Aug 27 11:11:05 2021

@author: janet
"""
             
import time
import matplotlib
import os
import pandas as pd
from watchdog.observers import Observer
from processing.preprocess import select_ROI_image
from processing.processing_functions import select_ROI
import matplotlib.pyplot as plt
#matplotlib.use('TkAgg') # This is for Mac
import numpy as np
from processing.RunAnalysisHandler import RunAnalysisHandler
import keyboard

#ROIs = [[3444, 2316,  480], [1096, 2484,  480], [2348, 1456,  480], [4352,  820,  480]]


## 1. DESCRIBING FOLDERS
framerate = 2
ORIGINAL_FOLDER = os.path.dirname(os.path.realpath(__file__))
print('THIS IS ORIGINAL FOLDER PATH', str(ORIGINAL_FOLDER))
IMG_FOLDER = os.path.abspath('images') #Folder where the images taken by the camera to be processed will be located
IMG_PROCESSED_FOLDER = os.path.abspath('images_processed')  #Folder where the resulting images will be located
DIR_ROI = os.path.abspath('focus')
path = IMG_FOLDER
os.chdir(path)
dirs = sorted(filter(os.path.isdir, os.listdir(path)), key=os.path.getctime)
os.chdir(ORIGINAL_FOLDER)
print(os.getcwd())
DIR = os.path.join(IMG_FOLDER, dirs[-1]) # folder to look at
print(os.getcwd())

# 2. SELECTING ROI from last image created in folder ./focus
ROI_path = select_ROI_image(DIR_ROI)  # selecting image to select ROI, getting path
print('ROI PATH', ROI_path)
os.chdir(ORIGINAL_FOLDER)  # going back to original working directory
ROIs = select_ROI(ROI_path)
time.sleep(1)


# 3. STARTING THE OBSERVER: it will find any new images
def run_analysis(ROI):
    # Observer for running the analysis
    observer = Observer()
    event_analysis_handler = RunAnalysisHandler(ROIs, window_size=5, IMG_FOLDER=IMG_FOLDER, framerate=framerate)  # create event handler
    observer.schedule(event_analysis_handler, path=DIR)  # set observer to use created handler in directory
    observer.start()  # creates a new thread
    print('TO_LOOK_FOLDER', DIR)


    # sleep until keyboard interrupt, then stop + rejoin the observer
    results_list = []

    fig = plt.figure()
    try:
        while True:
            time.sleep(0.1)  # keeps main thread running
            results_list = event_analysis_handler.get_result()
            print(results_list, 'results_list')
            foreground = [x[1] for x in results_list[1:]]
            background = [x[2] for x in results_list[1:]]
            timest= np.arange(0, framerate*len(foreground), framerate)
            print('Foreground,len', foreground, len(foreground))
            #plt.plot(timest, background)
            #plt.pause(1)
            #plt.show()
            #plt.clf()
            if keyboard.is_pressed('s'):  # if key 'q' is pressed  # if key 's' is pressed 
                print('You Pressed A Key!')
                observer.stop()  # when program stops, it does some work before terminating the thread
                print('last results list', results_list)
                # saving results as csv
                results_df = pd.DataFrame(results_list, columns=('Signal', 'Foreground', 'Background'))
                results_df.to_csv(str(DIR)+'/result.csv', index=True)
                quit()
                
    except (KeyboardInterrupt, SystemExit):  # When pressing ctrl-c (at the end of the acquisition)
        observer.stop()  # when program stops, it does some work before terminating the thread
        print('last results list', results_list)
        # saving results as csv
        results_df = pd.DataFrame(results_list, columns=('Signal', 'Foreground', 'Background'))
        results_df.to_csv(str(DIR)+'/result.csv', index=True)
        quit()
    observer.join() # is needed to proper end a thread for "it blocks the thread in which you're making the call, until (self.observer) is finished


    print('asdf', event_analysis_handler.get_result())
    quit()



run_analysis(ROIs)

