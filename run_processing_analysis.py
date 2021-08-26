#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RUN PRE-PROCESSING AND ANALYSIS

From saved images taken by SensUs 2021 device (SPR on AU-NHA)

Created on Sun Aug 22 11:12:06 2021

@author: janet


"""

import sys 
import os

path_code = os.path.dirname(__file__)

#important to import file that are not here
sys.path.append(os.path.abspath(path_code))

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk
from processing.processing_functions import temporal_mean_filter, save_imgs, temporal_median_filter, open_images, binarize_imgs, correct_background, select_ROI, invert_imgs, mask_ROIs
from analysis.Analyse_results_with_connected_components import Measure
#from analysis.Select_ROI import execute_roi
#from AcquireAndSave import execute_capture
#from AcquireAndDisplay import execute_focus





#%%

IMG_FOLDER = os.path.join('images') #Folder where the images taken by the camera to be processed will be located
IMG_PROCESSED_FOLDER = os.path.abspath('images_processed')  #Folder where the resulting images will be located


# 1. Select folder with images
root = Tk()
root.withdraw()
IMG_PATH = os.path.abspath(filedialog.askdirectory( title='Select Folder with images to be analyzed', initialdir = IMG_FOLDER))
print('\n Files to be processed in ', IMG_PATH)
NAME_IMG_FOLDER = os.path.basename(IMG_PATH)

# 2. Select image to use for placing the ROIs
root = Tk()
root.withdraw()
ROI_PATH = os.path.abspath(filedialog.askopenfilename(title='Select image to place ROI ', initialdir = IMG_PATH))
print('\n Selected image to place ROI ', ROI_PATH)


# 3. Opening images in directory folder
imgs = open_images(IMG_PATH)


#%%

## SELECT ROI
ROIs = select_ROI(ROI_PATH) 
#TODO: close image


#%%
## PRE-PROCESSING IMAGES

# 1. Temporal average filter: to remove moving objects
imgs_avg = temporal_mean_filter(imgs, 5)
#imgs_median = temporal_median_filter(imgs, 5)

# 2. Background illumination intensity correction
imgs_corrected = correct_background(imgs_avg)

# 3. Inverting image (our AU-NP spots will be white ~255)
imgs_inv = invert_imgs(imgs_corrected)
    
# 4. Binarizing images: we will have a binary image based on a threshold
rets, imgs_thresh = binarize_imgs(imgs_inv, tr = 180)   #TODO: FIND THRESHOLD

# 5. Applying a mask with the ROIs
imgs_masked = mask_ROIs(imgs_thresh, ROIs)


# View preprocessing
idx = -1
a = [imgs_avg[idx], imgs_corrected[idx], imgs_inv[idx], imgs_thresh[idx], imgs_masked[idx]]
titles = ["Avg", 'Background correction', 'inverted', 'binarized', 'mask ROI']

fig, axes = plt.subplots(2,3)
for i, ax in enumerate(axes.flat):
    c = ax.imshow(a[i], cmap='gray')
    fig.colorbar(c, ax = ax)
    ax.set_title(titles[i])



#%%
# Saving
SAVING_FOLDER = os.path.join(IMG_PROCESSED_FOLDER, NAME_IMG_FOLDER)
saving = False
if saving == True :
    save_imgs(imgs_avg, SAVING_FOLDER, NAME_IMG_FOLDER+'_avg_') # saving in a folder with the name of the original one but inside /images_processed
    #save_imgs(imgs_median, SAVING_FOLDER, NAME_IMG_FOLDER+'_median_')


#%%
# ANALYZING IMAGES
#Add here pipeline to analyse the images
capture_refresh_time = 2  # TODO!!!!!!!!
mes = Measure(NAME_IMG_FOLDER, ROIs, capture_refresh_time)
signal = mes.signal_perImage(imgs_avg[0], 80) #TODO: FOR LOOP AND DECIDE THRESHOLD, SAVE THIS IN .CSV



#%% To save/open the arrays
#par = np.array([imgs, imgs_avg, NAME_IMG_FOLDER, ROIs, ROI_PATH, IMG_PATH], dtype=object)
#with open('test.npy', 'wb') as f:
#    np.save(f, par)

with open('./test.npy', 'rb') as f:
    par = np.load(f, allow_pickle=True)

[imgs, imgs_avg, NAME_IMG_FOLDER, ROIs, ROI_PATH, IMG_PATH] = list(par)

#%% Test

######## Testing threshold
plt.figure()
plt.imshow(imgs_inv[0], cmap='gray')
thresholds = [0, 50, 80, 100, 120, 140, 160, 180, 200, 230]

fig, axes = plt.subplots(3,4)
for i, ax in enumerate(axes.flat):
    tr = thresholds[i]
    ret_test, img_thresh_test = cv2.threshold(imgs_inv[-1], tr, 255, cv2.THRESH_BINARY)
    c = ax.imshow(img_thresh_test, cmap='gray')
    fig.colorbar(c, ax = ax)
    ax.set_title('Threshold '+str(tr))

img = img_thresh_test.copy()

circles = ROIs[0]
spot = []

#plt.figure()
#plt.imshow(img, cmap='gray')

def find_GNP(img):
        ''' Function that will compute the connected components and return the number of components
        between 3-5 pixels TO BE DISCUSSED IF PIXELS CHANGE SIZE WITH PREPROCESSING
        Connected components of sizes 1 or 2 and above 30 will be disconsidered.
        
        returns: 
            nb_pixels: number of pixels corresponding to AU-NP
        '''
        print("shape image in find_GNP")
        print(img.shape)
        components = cv2.connectedComponentsWithStats(-1*img, 8, cv2.CV_32S)
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
                
                if((area>9) & (area<90)): #TODO: before it was 3, 30
                    nb_pixels = nb_pixels + area 
                
        return nb_pixels, labels
            

#def signal_perImage(img, tr):

spot = []
connectivity = 8 #changed: connectivity for connected components
"""
This function computes the signal given by the AU-NP, as number of pixels.
We first have a BW image which we threshold to separate the object from the background.
Then we find the connected components that correspond to the size of the AU-NP
"""



for cx, cy, rad in ROIs :
    #self.log.info('cx, cy, rad: {},{},{}'.format(cx, cy, rad))

    xvec, yvec = circle(cx,cy,rad) 
    
    
    #S,labs = find_GNP(thresh[circx,circy])
    S, labs = find_GNP(img[yvec, xvec])  # find AU-NP for the thresholded image, only in the ROIs (remember rows-columns vs x-y order)
    
    #plt.imshow(thresh_img[yvec, xvec])
    
    print('signal', S)
    spot.append(S)  #Changed
            
#        return spot, labs


# To view what there is
mask = np.zeros(img.shape)
mask[yvec,xvec]=True
img_masked = d*mask

