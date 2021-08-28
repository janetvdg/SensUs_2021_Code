#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 11:14:53 2021

@author: janet
"""


import sys 
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from processing.processing_functions import temporal_mean_filter, save_imgs, temporal_median_filter, open_images, binarize_imgs, correct_background, select_ROI, invert_imgs, mask_ROIs
from analysis.Analyse_results_with_connected_components import Measure
from skimage import io

# you input the images
# you input the threshold


def load_image(filename):
    imgs = [] # list with all the images (jpg or png)
    time_creation = [] # list with the time of creation of each image
    #parent = os.getcwd()
    #path = os.path.join(parent, PATH)
    print('\n Opening image '+str(filename)+' ...')
    
    #os.chdir(path)  #TODO: NOT SURE ABOUT THIS
    #files = sorted(filter(os.path.isfile, os.listdir(path)), key=os.path.getctime)  # ordering the images by date of creation

    
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        #img_path = os.path.join(path, filename)
        time_creation.append(os.stat(filename).st_ctime)
        #print(img_path)
        img = np.array(Image.open(filename))
        #imgs.append(img) #appending the image to the list
    elif filename.endswith('tiff') or filename.endswith('tif'):
        # img_path = os.path.join(path, filename)
        time_creation.append(os.stat(filename).st_ctime)
        # print(img_path)
        img = np.array(io.imread(filename))
        
    return img


def select_ROI_image(path):
    """
    Function to select the image to which select ROI
    :param path: path of the directory
    :return:
        path_ROI: path of the image
    """
    os.chdir(path)  #TODO: NOT SURE ABOUT THIS
    files = sorted(filter(os.path.isfile, os.listdir(path)), key=os.path.getctime)  # ordering the images by date of creation
    path_ROI = os.path.join(path, files[-1])  # getting the last one
    #print('\n Opening image to select ROI ' + str(filename) + ' ...')

    return path_ROI


def preprocess(imgs, window_size, threshold, ORIGINAL_FOLDER): 
    
    # 1. Temporal average filter: to remove moving objects
    imgs_avg = temporal_mean_filter(imgs, window_size)
    print('Averaged images shape: ', np.shape(imgs_avg))
    #imgs_median = temporal_median_filter(imgs, 5)
    
    # 2. Background illumination intensity correction
    imgs_corrected = correct_background(imgs_avg, ORIGINAL_FOLDER)  #TODO: WARNING IMGS_AVG
    print('Corrected images shape: ', np.shape(imgs_corrected))
    
    # 3. Inverting image (our AU-NP spots will be white ~255)
    imgs_inv = invert_imgs(imgs_corrected)
    print('Inverted images shape: ', np.shape(imgs_inv))
    
    # 4. Binarizing images: we will have a binary image based on a threshold
    rets, imgs_thresh = binarize_imgs(imgs_inv, threshold)   #TODO: FIND THRESHOLD
    print('Thresholded images shape: ', np.shape(imgs_thresh))
    
    return imgs_avg, imgs_thresh



def analysis(img, NAME_IMG_FOLDER, ROIs, framerate):
    mes = Measure(NAME_IMG_FOLDER, ROIs, framerate)
    result = mes.signal_perImage(img)
    signal = result[0]
    foreground = result[1]
    background = result[2]
    print('final signal', signal)
    
    return result

    
                                                                  
    #imgs_avg = temporal_mean_filter(imgs, threshold)
#    print('Averaged images shape: ', np.shape(imgs_avg))
#
#    #imgs_corrected = correct_background(imgs, ORIGINAL_FOLDER)  #TODO: WARNING IMGS_AVG
#    print('Corrected images shape: ', np.shape(imgs_corrected))                                                        




    
    



