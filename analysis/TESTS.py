# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 18:19:30 2021

@author: willi
"""
import os
import sys
import numpy as np
path = os.path.dirname(__file__) #sets the path of this current file
sys.path.append(os.path.abspath(path))

from AcquireAndSave import execute_capture
from AcquireAndDisplay import execute_focus
from Select_ROI import execute_roi
# Get the date and hour to make new folders
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
ROI_folder = str(now.strftime("%d_%m_%Y_%H_%M") + "_ROI")
results_folder = str(now.strftime("%d_%m_%Y_%H_%M") + "_results")


#Create the folder
dir = os.path.join(path,ROI_folder)
if not os.path.exists(dir):
    os.mkdir(dir)
    
dir = os.path.join(path,results_folder)
if not os.path.exists(dir):
    os.mkdir(dir)

#%% test

import cv2

img = cv2.imread(path_image, 0)
for circle in ROIs:
    cv2.circle(img, center=circle[:2], radius=circle[2],
                   color=(255,255,0), thickness=2)
    
    print("I am  drawing a circle")
    cv2.imshow('image', img)
    
#%% this is to test the circle function
from skimage.draw import circle

circx, circy = circle(100,500,10)
for cx, cy, rad in ROIs:
    print(cx,cy,rad)
    print("something")
    #%%
from Select_ROI import execute_roi
from Analyse_results import Measure
import numpy as np
path_image =  "C:/Sensus 2021/Code/SensUs_2021/Live_acquire/20_08_2021_13_16_ROI/1.png"
#path_image = os.path.join(path, ROI_folder)
# Original image size 5472 x 3648, we have to change its size to fit it on the computer
# As we don't analys this image we don't loose information
# We rescale the ROIs afterwards
RADIUS = 480 # You should't change this
scale_f = 4 # This you can adapt to your laptop
image_size = (int(5472/scale_f), int(3648/scale_f))
small_ROIs = execute_roi(path_image, image_size, int(RADIUS/scale_f))
ROIs = np.array(small_ROIs)*scale_f


#%% Now that the ROIs have been selected we need to analyse the results in our folder
capture_refresh_time = 2
mes = Measure("C:/Sensus 2021/Code/SensUs_2021/Live_acquire/20_08_2021_13_16_results/", ROIs, capture_refresh_time)
slope, concentration = mes.execute_analysis()
print(slope,concentration)
