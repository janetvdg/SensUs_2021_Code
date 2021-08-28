import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
import os
from preprocess import preprocess, load_image, analysis
from processing.processing_functions import select_ROI
from analysis.Analyse_results_with_connected_components import Measure



class RunROIHandler(FileSystemEventHandler):
    def __init__(self):
        self.ROIs = []
        #self.num_events = 0
        #self.imgs = []
        #self.ORIGINAL_FOLDER = os.getcwd()

    def on_created(self, event):  # when file is created
        # Every time a new image where the spots are seen is created in the focus folder, it counts the event, loads the image and runs select_ROI
        focus_img_path = event.src_path
        print('ROI image path', focus_img_path)
        #self.focus_img = load_image(filename)
        ## SELECT ROI
        #self.ROIs = select_ROI(focus_img_path)
        self.ROIs = [np.array([900, 900, 480]), np.array([200, 900, 480]), np.array([900, 200, 480])]
        return self.ROIs