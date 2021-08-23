# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 11:51:29 2021

@author: willi
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.draw import circle, circle_perimeter
from skimage import color
from skimage.filters import gaussian, threshold_otsu, threshold_minimum, sobel
from skimage.measure import label, regionprops
from skimage.morphology import closing, opening, disk, dilation
from skimage.io import ImageCollection, imread
from scipy import ndimage
from logging import getLogger


# Path is the path to the results folder
# Capture refresh time is the time between datapoints (after pre-processing)
# Circles is the center (x,y) and radius of the ROIs
# create a new variable tr which is the threshold we want to use after normalizing
class Measure:

    def __init__(self, path, circles, capture_refresh_time):
        self.path = path
        self.circles = circles
        self.capture_refresh_time = capture_refresh_time
        self.log = getLogger('main.Analysis')


    def signal_perImage(self, img,tr):

        spot = []
        for cx, cy, rad in self.circles :
            self.log.info('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            # print('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            circy, circx = circle(cx,cy,rad)
            print("This is x")
            print(circx)
            print("This is y")
            print(circy)
            #intensity_perSpot = img[circx, circy].mean()
            spot.append(np.mean(img[circx,circy] < tr)) # Note that we are counting pixels below threshold

        background = np.array(spot[-2:])
        self.log.info(f'background intensity: {background}')
        # print(f'background intensity: {background}')
        foreground = np.array(spot[:-2])
        self.log.info(f'foreground intensity: {foreground}')
        # print(f'foreground intensity: {foreground}')
        background_t = background.mean()
        foreground_t = foreground.mean()
        Signal = (foreground_t-background_t)#/(background+foreground)
        return Signal

# You get the intensityfrom inside the circles for all the different images
# What does sorted do
    def total_intensity(self):
        #ordered_id = sorted([int(file[4:8]) for file in os.listdir(self.path) \
                           #  if file[0:4] == 'img_' and file[-4:] == '.npy'])
        #ordered_pathes = [f'results/img_{n:04d}.npy' for n in ordered_id]
        #intensity = [self.intensity_perImage(np.load(f)) for f in ordered_pathes]
        intensity = []
        for img_arr in os.listdir(self.path) :
            #img = np.load(f)       
            intensity.append(self.signal_perImage(np.load(self.path + img_arr), 70))
            #del img
        return intensity
    
    
# Compute the increase of signal over time
    def compute_slope(self):
        y = self.total_intensity()
        x = (np.array(range(len(y))))*(self.capture_refresh_time)/60
        print(x)
        # We might need to change the fitting function
        reg_lin = np.polyfit(x, y, 1)
        return reg_lin[0]

# This function returns the concentration based on the previously obtained slope and 
    def get_concentration(self, slope):
        slope_calibration = -2446.18395303
        offset = 9.59393346
        concentration = slope*slope_calibration + offset
        if concentration < 0.5:
            return 0.5
        if concentration > 10:
            return 10
        return concentration

    def execute_analysis(self):
        slope = self.compute_slope()
        # print('slope: ',slope)

        concentration = self.get_concentration(slope)
        # print('concentration ',concentration)

        return slope, concentration
