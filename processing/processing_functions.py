# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 17:31:18 2021

@author: Janet
"""

import os
from PIL import Image
import numpy as np


# Opening images in directory folder
#imgs = [] # list with all the images (jpg or png)
#directory = r'../../test_preproc'  #TODO: Change to wanted directory
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
#    

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
#imgs_avg = temporal_mean_filter(imgs, 5)
#print('Saving images filtered with a temporal average filter...')
#for i in np.arange(0, len(imgs_avg)):
#    Image.fromarray(imgs_avg[i]).save('avg_'+str(i)+'.png')
#    





#mean of all images or take median filter (removing moving objects)
#remove background: 2nd or 3rd polynomial
#threshold every pixel: determining it manually looking at pixel
        
# Histogram
    
    
# images normalized to 1
    




#%%Background smoothing functions (from SensUs 2019)
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rescale
from skimage.feature import peak_local_max
from numpy.polynomial import polynomial
from numpy.polynomial.polynomial import polyval2d



def polyfit2d(x, y, f, deg):   #TODO: TRY THIS POLY TO IMAGE WITH ONLY LIGHT
    '''
    Fits a 2d polynomial of degree deg to the points f where f is the value of point [x,y]
    '''
    x = np.asarray(x)
    y = np.asarray(y)
    f = np.asarray(f)
    deg = np.asarray(deg)
    vander = polynomial.polyvander2d(x, y, deg)
    vander = vander.reshape((-1, vander.shape[-1]))
    f = f.reshape((vander.shape[0],))
    c = np.linalg.lstsq(vander, f, rcond=None)[0]
    return c.reshape(deg+1)


def smooth_background(img, rescale_factor=0.1, poly_deg=[2,2]):
    '''
    Smooths the background of the image by modeling the background with a polynomial 
    surface by regression on the local maximum intensity peaks and dividing the original
    image by this surface.
    Parameters
    ----------
    img : ndarray
        Image.
    rescale_factor : float or int, optional
        The scaling of the image used to fit the polynomial surface. The default is 0.1.
    poly_deg : list or double, optional
        List where the first and secong elements are the polynomial degrees on the x and y axis respectively. The default is [1,2].
    Returns
    -------
    the input image with smoothed background.
    '''

    imgs = rescale(img, rescale_factor, preserve_range=True)
    BW = peak_local_max(imgs, indices=False)
    k = BW*imgs
    
    ind = np.nonzero(k)
    z = k[ind]
    
#TODO watch out polynomial degree might change depending on background. We chose [1, 2], because deformation looked "cylindrical"
#   but [2, 2] or other could make sense depending on deformation.
    p = polyfit2d(ind[0],ind[1],z, poly_deg)
    xx, yy = np.meshgrid(np.linspace(0, imgs.shape[0], img.shape[0]), 
                         np.linspace(0, imgs.shape[1], img.shape[1]))

    background = np.transpose(polyval2d(xx, yy, p))
    return background





#test = imgs[0]
#background = smooth_background(test)
#plt.imshow(background)




## ANALYZING IMAGES
# Now that the ROIs have been selected we need to analyse the results in our folder
#capture_refresh_time = 2 # TODO
#mes = Measure(results_folder, ROIs, capture_refresh_time)
#slope, concentration = mes.execute_analysis()
#print(slope,concentration)