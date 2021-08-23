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

#Added
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
        Connected components of sizes 1 or 2 and above 30 will be disconsidered
        '''
        components = cv2.connectedComponentsWithStats(img, 8, cv2.CV_32S)
        num_labels = components[0]  # number of labels
        labels = components[1]      # label matrix, where each pixel in the same connected component gets the same value
        stats = components[2]       # stat matrix
        centroids = components[3]   # centroid matrix
        
        nb_pixels = 0
        
        for c in range(0, num_labels):
            if c == 0:
                print("background")
            else:
                ("print not background")
                area = stats[c, cv2.CC_STAT_AREA]
                if((area>3) & (area<30)):
                    nb_pixels = nb_pixels + area 
                
        return nb_pixels
            
    def signal_perImage(self, img,tr):

        spot = []
        connectivity = 8 #changed: connectivity for connected components
        for cx, cy, rad in self.circles :
            self.log.info('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            # print('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            circy, circx = circle(cx,cy,rad) 
            print("This is x")
            print(circx)
            print("This is y")
            print(circy)
            #intensity_perSpot = img[circx, circy].mean()
            #spot.append(np.mean(img[circx,circy] < tr)) # Note that we are counting pixels below threshold
            #For this to work we need to binarise the image too
            spot.append(find_GNP(self, img[circx,circy]))  #Changed
        
        
        background = np.sum(np.array(spot[-2:])) #cnaged to sum 
        self.log.info(f'background intensity: {background}')
        # print(f'background intensity: {background}')
        foreground = np.sum(np.array(spot[:-2])) #changed to sum 
        self.log.info(f'foreground intensity: {foreground}')
        # print(f'foreground intensity: {foreground}')
        #background_t = background.mean()
        #foreground_t = foreground.mean()
        #Signal = (foreground_t-background_t)/(background+foreground)
        Signal = foreground/background * 100
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
#%% Test
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

#Added
import cv2

circles = np.array([[315, 400, 50]])
spot = []
def find_GNP(img):
        ''' Function that will compute the connected components and return the number of components
        between 3-5 pixels TO BE DISCUSSED IF PIXELS CHANGE SIZE WITH PREPROCESSING
        Connected components of sizes 1 or 2 and above 30 will be disconsidered
        '''
        print("shape image in find_GNP")
        print(img.shape)
        components = cv2.connectedComponentsWithStats(img, 8, cv2.CV_32S)
        num_labels = components[0]  # number of labels
        labels = components[1]      # label matrix, where each pixel in the same connected component gets the same value
    
        stats = components[2]       # stat matrix
        centroids = components[3]   # centroid matrix
        
        nb_pixels = 0
        for c in range(0, num_labels):
            if c == 0:
                print("background")
            else:
                print("Signal")
                area = stats[c, cv2.CC_STAT_AREA]
                
                if((area>3) & (area<30)):
                    nb_pixels = nb_pixels + area 
                
        return nb_pixels, labels
            

def signal_perImage(img,tr):

        spot = []
        labs = []
        thresh = []
        connectivity = 8 #changed: connectivity for connected components
        for cx, cy, rad in circles :
            #self.log.info('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            # print('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            circy, circx = circle(cx,cy,rad) 
            # print("This is x")
            # print(circx)
            # print("This is y")
            # print(circy)
            #intensity_perSpot = img[circx, circy].mean()
            #spot.append(np.mean(img[circx,circy] < tr)) # Note that we are counting pixels below threshold
            #For this to work we need to binarise the image too
            ret, thresh = cv2.threshold(img,tr,255,cv2.THRESH_BINARY)
            thresh = thresh[:,:,0]
            print("Shape threshold")
            print(thresh.shape)
            print("")
            #S,labs = find_GNP(thresh[circx,circy])
            S,labs = find_GNP(thresh)
            print(S)
            spot.append(S)  #Changed
            
        return spot, labs


#%%
src = cv2.imread('C:/Sensus 2021/Code/Code_23_08/Binary.png')
print(src.shape)
S, lable = signal_perImage(src, 80)

#%% 
#cv2.imshow('image', src)

