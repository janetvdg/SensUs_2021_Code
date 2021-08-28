# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 10:51:14 2021

@author: willi
"""
#%% Import the relevant files
#File with everything

# At the moment we are intialising the camera 2x which is very annoying
import os
import sys
import numpy as np
path = os.path.dirname(__file__) #sets the path of this current file
sys.path.append(os.path.abspath(path))

from AcquireAndSave import execute_capture
from AcquireAndDisplay import execute_focus
from Select_ROI import execute_roi
from Analyse_results import Measure

# Get the date and hour to make new folders
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
ROI_folder = str(now.strftime("%d_%m_%Y_%H_%M") + "_ROI\\")
results_folder = str(now.strftime("%d_%m_%Y_%H_%M") + "_results\\")


#Create the folder
dir = os.path.join(path,ROI_folder)
if not os.path.exists(dir):
    os.mkdir(dir)
    
dir = os.path.join(path,results_folder)
if not os.path.exists(dir):
    os.mkdir(dir)
#%% This cell gives you the images to set the focus and save the last
# image you see at the end of the focus into ROI_folder
execute_focus(ROI_folder)

#%% Once the focus is set we can acquire one image to see the 
# Need to fix: results folder is empty at the moment

execute_capture(results_folder)

#%% For the moment we are using a test folder
path_image = ROI_folder + "1.png"
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
mes = Measure(results_folder, ROIs, capture_refresh_time)
slope, concentration = mes.execute_analysis()
print(slope,concentration)
