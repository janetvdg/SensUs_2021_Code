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


class RunAnalysisHandler(FileSystemEventHandler):
    def __init__(self, ROIs, IMG_FOLDER, window_size=5, threshold=130, framerate = 2):
        self.num_events = 0
        self.window_size = window_size
        self.threshold = threshold
        self.imgs = []
        self.ORIGINAL_FOLDER = os.getcwd()
        self.framerate = framerate
        self.results = []
        self.ROIs = ROIs
        self.IMG_FOLDER = IMG_FOLDER

    def on_created(self, event):  # when file is created
        # Every time a new file is created in the folder, it counts the event and loads the image
        self.num_events += 1
        filename = event.src_path
        self.imgs.append(load_image(filename))

        # If the number of events is lower than the threshold, it will only load the image
        if self.num_events < self.window_size:
            # print("Got event for file %s" % event.src_path)
            print('imgs', np.shape(self.imgs))

        # If the number of events is equal to the window size, it will preprocess the list of images
        else:
            img_avg, img_thresh = preprocess(self.imgs, self.window_size, self.threshold, self.ORIGINAL_FOLDER)
            signal = []
            foreground = []
            background = []

            mes = Measure(self.IMG_FOLDER, self.ROIs, self.framerate)
            self.result.append(mes.signal_perImage(img_thresh))
            signal = self.result[0]
            foreground = self.result[1]
            background = self.result[2]
            print('final signal', signal)


            # Reinitializing the count and the list of images
            print(self.num_events)
            self.num_events = 0
            print(self.num_events)
            self.imgs = []  # restarting the list


class RunROIHandler(FileSystemEventHandler):
    def __init__(self):
        self.ROIs = []
        #self.num_events = 0
        #self.imgs = []
        #self.ORIGINAL_FOLDER = os.getcwd()

    def on_created(self, event):  # when file is created
        # Every time a new image where the spots are seen is created in the focus folder, it counts the event, loads the image and runs select_ROI
        focus_img_path = event.src_path
        print('ROI image path', focus_img_path)
        #self.focus_img = load_image(filename)
        ## SELECT ROI
        self.ROIs = select_ROI(focus_img_path)





    ## TODO: MAKE SELECT THE DIRECTORY TO WHICH FIND THE IMAGES


ROIs = [np.array([900, 900, 480]), np.array([200, 900, 480]), np.array([900, 200, 480])]

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
print('TO_LOOK_FOLDER', DIR)
# moving average of the signal result



# 2. STARTING THE OBSERVER: it will find any new images
# Observer for selecting ROI
#observer1 = Observer()
#event_ROI_handler = RunROIHandler() # create event handler
#print('path DIR ROI', DIR_ROI)
#observer1.schedule(event_ROI_handler, path=DIR_ROI) # set observer to use created handler in directory
#observer1.start()

# Observer for running the analysis
observer2 = Observer()
event_analysis_handler = RunAnalysisHandler(ROIs, window_size = 5, IMG_FOLDER = IMG_FOLDER) # create event handler
observer2.schedule(event_analysis_handler, path=DIR) # set observer to use created handler in directory
observer2.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()




#TODO: ROI