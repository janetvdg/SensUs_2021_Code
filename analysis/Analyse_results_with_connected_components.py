# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 11:51:29 2021
@author: willi+deborah
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
import cv2


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

    def find_GNP(self, img): 
        ''' Function that will compute the connected components and return the number of components
        between 3-5 pixels TO BE DISCUSSED IF PIXELS CHANGE SIZE WITH PREPROCESSING
        Connected components of sizes 1 or 2 and above 30 will be disconsidered.
        
        An AU-NP is considered as a connected component with size between ????? TODO
         
        input:
            img: 1-D array with intensity values at the ROI area
        returns: 
            nb_pixels: number of pixels corresponding to AU-NP
            percent_pixels: percentage of pixels that correspond to a connected component
            labels: label matrix, where each pixel in the same connected component gets the same value
        '''

        components = cv2.connectedComponentsWithStats(img, 8, cv2.CV_32S)
        num_labels = components[0]  # number of labels
        labels = components[1]      # label matrix, where each pixel in the same connected component gets the same value
        stats = components[2]       # stat matrix
        centroids = components[3]   # centroid matrix
        
        nb_pixels = 0
        for c in range(0, num_labels):
            if c == 0:
                #print("background")
                continue
            else:
                #print("Signal")
                area = stats[c, cv2.CC_STAT_AREA]
                if((area>9) & (area<90)): #TODO: before it was 3, 30
                    nb_pixels = nb_pixels + area 
                    
        percent_pixels = nb_pixels /len(img)
        print('Number of pixels detected: ', nb_pixels)
        print('Percentage of pixels detected: ', percent_pixels*100, '%')
        
        return nb_pixels, percent_pixels, labels
            
    # TODO: FIND BACKGROUND
    # TODO: SAVE ARRAY OF NUMBER OF PIXELS FOR EACH IMAGE

    
    def signal_perImage(self, img):

        spot = []
        connectivity = 8 #connectivity for connected components
        for cx, cy, rad in self.circles :
            self.log.info('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            xvec, yvec = circle(cx, cy, rad)  #TODO: CHANGE TO DISK, SOME PROBLEMS HERE WITH SIZE
            S, percent_pixels, labels = self.find_GNP(img[yvec, xvec])
            spot.append(S)  #Changed
        
        
        background = np.sum(np.array(spot[-2:])) #changed to sum 
        self.log.info(f'background intensity: {background}')
        # print(f'background intensity: {background}')
        foreground = np.sum(np.array(spot[:-2])) #changed to sum 
        self.log.info(f'foreground intensity: {foreground}')
        # print(f'foreground intensity: {foreground}')
        #background_t = background.mean()
        #foreground_t = foreground.mean()
        #Signal = (foreground_t-background_t)/(background+foreground)
        print('background', background)
        print('foreground', foreground)
        print('spot', spot)
        Signal = foreground/background * 100
        return Signal, foreground, background
    
           
        

# You get the intensity from inside the circles for all the different images
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


#%%
#src = cv2.imread('C:/Sensus 2021/Code/Code_23_08/Binary.png')
#print(src.shape)
#S, lable = signal_perImage(src, 80)

#%% 
#cv2.imshow('image', src)