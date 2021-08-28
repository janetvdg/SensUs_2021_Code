
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
import os
from preprocess import preprocess, load_image, analysis
from processing.processing_functions import select_ROI
from analysis.Analyse_results_with_connected_components import Measure
import matplotlib.pyplot as plt

class RunAnalysisHandler(FileSystemEventHandler):
    def __init__(self, ROIs, IMG_FOLDER, window_size=5, threshold=130, framerate = 2):
        self.num_events = 0
        self.window_size = window_size
        self.threshold = threshold
        self.imgs = []
        self.ORIGINAL_FOLDER = os.getcwd()
        self.framerate = framerate
        self.result = []
        self.ROIs = ROIs
        self.IMG_FOLDER = IMG_FOLDER
        self.results_list = [[]]
        self.log = False

    def process_analyse(self):
        img_avg, img_thresh = preprocess(self.imgs, self.window_size, self.threshold, self.ORIGINAL_FOLDER)
        signal = []
        foreground = []
        background = []

        mes = Measure(self.IMG_FOLDER, self.ROIs, self.framerate)
        self.result = mes.signal_perImage(img_thresh[0]) # I select 0 because it's a list with one single element
        signal = self.result[0]
        foreground = self.result[1]
        background = self.result[2]
        print('final signal', signal)
        return self.result

    def on_created(self, event):  # when file is created
        # Every time a new file is created in the folder, it counts the event and loads the image
        self.num_events += 1
        filename = event.src_path
        self.imgs.append(load_image(filename))

        # If the number of events is lower than the threshold, it will only load the image
        if self.num_events < self.window_size:
            # print("Got event for file %s" % event.src_path)
            print('imgs', np.shape(self.imgs))
            self.log = False

        # If the number of events is equal to the window size, it will preprocess the list of images
        else:
            self.process_analyse()
            self.results_list.append(list(self.result))
            self.log = True
            # Reinitializing the count and the list of images
            self.num_events = 0
            self.imgs = []  # restarting the list


    def get_result(self):
        return self.results_list
