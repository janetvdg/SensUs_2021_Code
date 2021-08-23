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
from utilities import smooth_background
from scipy import ndimage
from logging import getLogger

class Measure:


    def __init__(self, path, circles):
        self.path = path
        self.circles = circles
        self.log = getLogger('main.Analysis')


    def high_pass(img):
        lowpass = ndimage.gaussian_filter(img, 8)
        gauss_highpass = img - lowpass
        return gauss_highpass

    def high_pass2(img):
        kernel = np.array([[-1, -1, -1, -1, -1],
                       [-1,  1,  2,  1, -1],
                       [-1,  2,  4,  2, -1],
                       [-1,  1,  2,  1, -1],
                       [-1, -1, -1, -1, -1]])

        highpass_5x5 = ndimage.convolve(img, kernel)
        return highpass_5x5


    def intensity_perImage(self, img):

        spot = []
        for cx, cy, rad in self.circles :
            self.log.info('cx, cy, rad: {},{},{}'.format(cx, cy, rad))
            circy, circx = circle(cx,cy,rad)
            intensity_perSpot = img[circx, circy].mean()
            spot.append(intensity_perSpot)

        background = np.array(spot[-2:])
        self.log.info(f'background intensity: {background}')
        foreground = np.array(spot[:-2])
        self.log.info(f'foreground intensity: {foreground}')
        background = background.mean()
        foreground = foreground.mean()
        intensity_per_image = (background-foreground)/(background+foreground)
        return intensity_per_image


    def total_intensity(self):
        ordered_id = sorted([int(file[4:8]) for file in os.listdir(self.path) \
                             if file[0:4] == 'img_' and file[-4:] == '.npy'])
        ordered_pathes = [f'results/img_{n:04d}.npy' for n in ordered_id]
        #intensity = [self.intensity_perImage(np.load(f)) for f in ordered_pathes]
        intensity = []
        for f in ordered_pathes :
            img = np.load(f)
            intensity.append(self.intensity_perImage(img))
            del img
        return intensity

    def compute_slope(self):
        y = self.total_intensity()
        x = range(len(y))
        reg_lin = np.polyfit(x, y, 1)
        return reg_lin[0], y

    def get_concentration(self):
        slope_calibration = 5.0;
        return self.compute_slope()*slope_calibration


    def run(self):

        slope = self.compute_slope()
        print(slope)

        concentration = self.get_concentration()
        print(concentration)

        #concentration + slope
        return slope, concentration
