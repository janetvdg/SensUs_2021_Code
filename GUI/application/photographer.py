from threading import Thread, Event, Lock
from queue import Queue, Full, Empty
import time
from logging import getLogger
from . import acquisition
import numpy as np


class Photographer(Thread):

    # !! FROM THE OUTSIDE, ONLY CALL start(), set_mode(...), is_finished()
    # !! has_new_live_image(), get_new_live_image(), get_progess() and stop()

    def __init__(self, capture_path='results/img_', n_acquisitions=4,
                 live_stream_fps=24, capture_refresh_time=30):
        Thread.__init__(self)
        self.log = getLogger('main.Photographer')
        self.log.debug('Photographer created')
        self.mode_queue = Queue()
        self.live_image_queue = Queue(8)
        self.live_stream_fps = live_stream_fps
        self.capture_refresh_time = capture_refresh_time
        self.capture_path = capture_path
        self.n_acquisitions = n_acquisitions
        self.acquisition = None
        self.acquisition_c = None
        self._acquisition_i = 0
        self._acquisition_i_lock = Lock()
        self.mode = None
        self.t_st=time.process_time()
        self.quitting = Event()
        self._start_time = None
        self._start_time_lock = Lock()

    @property
    def start_time(self):
        with self._start_time_lock:
            return self._start_time

    @start_time.setter
    def start_time(self, t):
        with self._start_time_lock:
            self._start_time = t

    @property
    def acquisition_i(self):
        with self._acquisition_i_lock:
            return self._acquisition_i

    @acquisition_i.setter
    def acquisition_i(self, i):
        with self._acquisition_i_lock:
            self._acquisition_i = i

    def get_progress(self):
        start_time = self.start_time
        total_time = self.n_acquisitions * self.capture_refresh_time
        if start_time is None:
            return 0
        time_progress = max(min((time.process_time() - start_time) / total_time, 1), 0)
        n_img_progress = self.acquisition_i / self.n_acquisitions
        return n_img_progress

    def is_finished(self):
        return self.acquisition_i == self.n_acquisitions

    def set_mode(self, m):
        if m not in (None, 'live_stream', 'capture'):
            raise KeyError(m)
        self.log.debug(f'Putting mode: {m}')
        self.mode_queue.put(m)
        self.log.debug(f'Put mode: {m}')

    def has_new_live_image(self):
        return self.live_image_queue.empty() is not True

    def get_new_live_image(self):
        return self.live_image_queue.get(False)

    def run(self):
        self.log.debug('Photographer start')
        t_live = 0
        t_capt = 0

        while not self.quitting.is_set():

            # get new mode
            while not self.mode_queue.empty():
                try:
                    self._set_mode(self.mode_queue.get(block=False))
                    print(f'Mode set to {self.mode}')
                    self.log.debug(f'Mode set to {self.mode}')
                except Empty:
                    pass

            # capture
            if self.mode == 'capture':
                #if id(self.acquisition)!=id(None):
                if hasattr(self, 'acquisition'):
                    del self.acquisition
                self.log.debug('Photographe capture')
                try:
                    #self.capture()
                    flag=True
                    print('s')
                    self.acquisition_c= acquisition.Capture(expo_time=self.expo_time)
                    while flag:
                        if time.process_time() - self.t_st > self.capture_refresh_time:
                            print('real time fps',1/(time.process_time()-self.t_st))
                            img = self.acquisition_c.get_image()
                            self.t_st = time.process_time()
                            self.log.info(f'capture res: {img.shape}')
                            path = self.capture_path + f"{self.acquisition_i:04d}"
                            np.save(path, img)
                            print(time.process_time())
                            self.log.debug(f'Capture to "{path}"')
                            self.acquisition_i += 1
                            if self.acquisition_i >= self.n_acquisitions:
                                flag=False
                                self.log.info('Capture mode ended')
                                self.mode = 'live_stream'   
                    del self.acquisition_c
                    self.acquisition = acquisition.LiveStream()
                except BaseException as e:
                    self.log.debug(f'Failed to captura: {e}')

            #livestream
            if self.mode=='live_stream' \
                    and time.process_time() - t_live > 1 / self.live_stream_fps:
                t_live = time.process_time()
                self.log.debug('Photographe live_stream')
                try:
                    self.live_stream()
                except BaseException as e:
                    self.log.debug(f'Failed to live stream: {e}')

    def stop(self):
        self.log.debug('stop signal')
        self.quitting.set()

    def capture(self):
        try:
            del self.acquisition
            self.acquisition = acquisition.Capture(expo_time=self.expo_time)
            img = self.acquisition.get_image()
            self.log.info(f'capture res: {img.shape}')
            path = self.capture_path + f"{self.acquisition_i:04d}"
            np.save(path, img)
            print(time.process_time())
            self.log.debug(f'Capture to "{path}"')
            self.acquisition_i += 1
            if self.acquisition_i >= self.n_acquisitions:
                self.log.info('Capture mode ended')
                self.mode = 'live_stream'
            del self.acquisition
            self.acquisition = acquisition.LiveStream()
        except BaseException as e:
            self.log.exception(f'Capture acquisition failed {e}')

    def live_stream(self):
        try:
            if self.mode:
                del self.acquisition
            self.acquisition = acquisition.LiveStream()
            live_image = self.acquisition.get_image()
            try:
                self.live_image_queue.put(live_image, False)
            except Full:
                self.log.warn('Live stream frame drop, (queue is full)')
        except BaseException as e:
            self.log.exception(f'Live stream acquisition failed {e}')

    def _set_mode(self, m):
        try:
            if m not in ('capture', 'live_stream', None):
                raise KeyError(m)
            self.log.debug(f'Setting acquisition mode to "{m}"')
            self.mode = m

            if m == 'capture':
                self.start_capture_mode()
            if m == 'live_stream':
                self.start_live_stream_mode()

        except BaseException as e:
            self.log.exception(f'Failed to switch to mode {m}: {e}')

    def start_capture_mode(self):
        self.acquisition_i = 0
        self.start_time = time.process_time()
        del self.acquisition
        self.acquisition = acquisition.Capture()
        self.expo_time = self.acquisition.get_exposure_time()
        self.log.info(f'New expo time: {self.expo_time}us')
        del self.acquisition
        self.acquisition = acquisition.LiveStream()

    def start_live_stream_mode(self):
        del self.acquisition
        self.acquisition = acquisition.LiveStream()
