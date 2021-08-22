# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 17:31:18 2021

@author: Janet
"""

import os
from PIL import Image
import numpy as np


# Opening images in directory folder
imgs = [] # list with all the images (jpg or png)
directory = r'../../test_preproc'  #TODO: Change to wanted directory
print('Opening images '+str(os.listdir(directory))+'...')
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        img_path = os.path.join(directory, filename)
        #print(img_path)
        img = np.array(Image.open(img_path))
        imgs.append(img) #appending the image to the list
        
    else:
        continue
    

def temporal_median_filter(imgs, size_kernel):
    """ Temporal median filter
    
    Performs temporal median filter without overlapping.
    Warning: if the number of images is not a multiple of the kernel size, the last images will be lost.
    
    imgs: list of images to process
    size_kernel: number of frames over which computes median filter
    
    """
    print('\n Computing temporal median filter with kernel size ', size_kernel, '...')
    imgs_med = []
   
    for i in np.arange(0, len(imgs)//size_kernel-size_kernel) :  
        try:
            seq = np.stack(imgs[i*(size_kernel+1):(size_kernel*(i+1)+i)], axis = 2)  #TODO: use last images as well
            batch = np.median(seq, axis = 2).astype(np.uint8)
            imgs_med.append(batch)
        except:
            print('Could not compute window with indices '+str(i*(size_kernel+1))+' to '+ str((size_kernel*(i+1)+i)))
            
    return imgs_med


def temporal_mean_filter(imgs, size_kernel):
    """ Temporal mean filter
    
    Performs temporal average filter without overlapping
    
    imgs: list of images to process
    size_kernel: number of frames over which computes median filter
    
    """
    print('\n Computing temporal average filter with kernel size ', size_kernel, '...')
    imgs_med = []
    
    for i in np.arange(0, len(imgs)//size_kernel-size_kernel) :
        print('Computing window from '+str(i*(size_kernel+1))+' to '+ str((size_kernel*(i+1)+i)))
        try: 
            seq = np.stack(imgs[i*(size_kernel+1):(size_kernel*(i+1)+i)], axis = 2)  #TODO: use last images as well
            batch = np.mean(seq, axis = 2).astype(np.uint8)
            imgs_med.append(batch)
        except:
            print('Could not compute window with indices '+str(i*(size_kernel+1))+' to '+ str((size_kernel*(i+1)+i)))
    
    return imgs_med


# Median
#imgs_med = temporal_median_filter(imgs, 5)
#print('Saving images filtered with a temporal median filter...')
#for i in np.arange(0, len(imgs_med)):
#    Image.fromarray(imgs_med[i]).save('median_'+str(i)+'.png')
# 
  
# Average
imgs_avg = temporal_mean_filter(imgs, 5)
print('Saving images filtered with a temporal average filter...')
for i in np.arange(0, len(imgs_avg)):
    Image.fromarray(imgs_avg[i]).save('avg_'+str(i)+'.png')
    





#mean of all images or take median filter (removing moving objects)
#remove background: 2nd or 3rd polynomial
#threshold every pixel: determining it manually looking at pixel
        
# Histogram
    
    
# images normalized to 1