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
from processing.processing_functions import temporal_mean_filter
from analysis.Analyse_results import Measure

#from AcquireAndSave import execute_capture
#from AcquireAndDisplay import execute_focus
#from Select_ROI import execute_roi
#from Analyse_results import Measure




## OPENING FILES
# Opening images in directory folder
#imgs = [] # list with all the images (jpg or png)
#directory = r'./test_preproc'  #TODO: Change to wanted directory
#print('Opening images '+str(os.listdir(directory))+'...')
#for filename in os.listdir(directory):
#    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
#        img_path = os.path.join(directory, filename)
#        #print(img_path)
#        img = np.array(Image.open(img_path))
#        imgs.append(img) #appending the image to the list
#        
#    else:
#        continue
    
    
## PRE-PROCESSING IMAGES
#1. Temporal average filter
imgs_avg = temporal_mean_filter(imgs, 5)

#2. Homogenizing incident light to have a flat background: background illumination intensity correction



## ANALYZING IMAGES
# Now that the ROIs have been selected we need to analyse the results in our folder
#capture_refresh_time = 2 # TODO
#mes = Measure(results_folder, ROIs, capture_refresh_time)
#slope, concentration = mes.execute_analysis()
#print(slope,concentration)


    


