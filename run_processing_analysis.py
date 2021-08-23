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
from processing.processing_functions import temporal_mean_filter
from analysis.Analyse_results import Measure
#from AcquireAndSave import execute_capture
#from AcquireAndDisplay import execute_focus
from analysis.Select_ROI import execute_roi  #TODO: SOMETIMES THIS DOES NOT WORK
#from Analyse_results import Measure




#%%
## OPENING FILES
IMG_FOLDER = os.path.join('images') #Folder where the images taken by the camera to be processed will be located
IMG_PROCESSED_FOLDER = os.path.join('images_processed')  #Folder where the resulting images will be located


# 1. Select folder with images
root = Tk()
root.withdraw()
IMG_PATH = os.path.abspath(filedialog.askdirectory(title='Select Folder with images to be analyzed', initialdir = IMG_FOLDER))
print('\n Files to be processed in ', IMG_PATH)

# 2. Select image to use for placing the ROIs
root = Tk()
root.withdraw()
ROI_PATH = os.path.abspath(filedialog.askopenfilename(title='Select image to place ROI ', initialdir = IMG_PATH))
print('\n Selected image to place ROI ', ROI_PATH)



# Opening images in directory folder
def open_images(path):
    imgs = [] # list with all the images (jpg or png)
    print('\n Opening images '+str(path)+'...')
    #for filename in os.listdir(directory):
    for filename in os.listdir(path):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            img_path = os.path.join(path, filename)
            #print(img_path)
            img = np.array(Image.open(img_path))
            imgs.append(img) #appending the image to the list
            
        else:
            continue
    return imgs
    
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
imgs_avg = temporal_mean_filter(imgs, 5)

#2. Homogenizing incident light to have a flat background: background illumination intensity correction



## ANALYZING IMAGES
# Add here pipeline to analyse the images


    


