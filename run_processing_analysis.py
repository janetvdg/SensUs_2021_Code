#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RUN PRE-PROCESSING AND ANALYSIS

From saved images taken by SensUs 2021 device (SPR on AU-NHA)

Created on Sun Aug 22 11:12:06 2021

@author: janet
"""


import os
from PIL import Image
import numpy as np
from tkinter import filedialog, Tk
from processing.processing_functions import temporal_mean_filter, save_imgs, temporal_median_filter, open_images
from analysis.Analyse_results import Measure
#from AcquireAndSave import execute_capture
#from AcquireAndDisplay import execute_focus
from analysis.Select_ROI import execute_roi  #TODO: SOMETIMES THIS DOES NOT WORK
#from Analyse_results import Measure




#%%
## OPENING FILES
IMG_FOLDER = os.path.join('images') #Folder where the images taken by the camera to be processed will be located
IMG_PROCESSED_FOLDER = os.path.abspath('images_processed')  #Folder where the resulting images will be located


# 1. Select folder with images
root = Tk()
root.withdraw()
IMG_PATH = os.path.abspath(filedialog.askdirectory(title='Select Folder with images to be analyzed', initialdir = IMG_FOLDER))
print('\n Files to be processed in ', IMG_PATH)
NAME_IMG_FOLDER = os.path.basename(IMG_PATH)

# 2. Select image to use for placing the ROIs
root = Tk()
root.withdraw()
ROI_PATH = os.path.abspath(filedialog.askopenfilename(title='Select image to place ROI ', initialdir = IMG_PATH))
print('\n Selected image to place ROI ', ROI_PATH)


# 3. Opening images in directory folder
print('hello')
imgs = open_images(IMG_PATH)




 #%% 
    
## SELECT ROI
RADIUS = 480 # You should't change this
scale_f = 4 # This you can adapt to your laptop
image_size = (int(5472/scale_f), int(3648/scale_f))
small_ROIs = execute_roi(ROI_PATH, image_size, int(RADIUS/scale_f))  # returned as x, y, radius
ROIs = np.array(small_ROIs)*scale_f  # x, y, radius
print('ROIs', ROIs)

  
#%%  
## PRE-PROCESSING IMAGES
#1. Temporal average filter
#imgs_avg = temporal_mean_filter(imgs, 5)
imgs_median = temporal_median_filter(imgs, 5)

#2. Homogenizing incident light to have a flat background: background illumination intensity correction

# Saving
SAVING_FOLDER = os.path.join(IMG_PROCESSED_FOLDER, NAME_IMG_FOLDER) 
#save_imgs(imgs_avg, SAVING_FOLDER, NAME_IMG_FOLDER+'_avg_') # saving in a folder with the name of the original one but inside /images_processed
save_imgs(imgs_median, SAVING_FOLDER, NAME_IMG_FOLDER+'_median_')


## ANALYZING IMAGES
# Add here pipeline to analyse the images


    


