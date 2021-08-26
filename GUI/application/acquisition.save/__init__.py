from . import camera as cam
import numpy as np
from logging import getLogger


class Acquistion:

    def __init__(self, live_fps=24, live_res=(800, 533), expo_max=15000):
        self.log = getLogger('main.acquisition')
        self.log.debug('Creating acquisition')
        self.cam = cam.Camera()
        self.setup_basic()
        self.live_fps = live_fps
        self.live_res = live_res
        self.expo_max = expo_max
        self._mode = None
        self.expo_time = None

    def autoset_exposure_time(self):
        self.expo_time = 15000

    def get_capture_image(self):
        self.mode = 'capture'
        self.cam.BeginAcquisition()
        image = cam.GetNextImage()
        if image.IsIncomplete():
            status = image.GetImageStatus()
            self.log.error(f'Image incomplete, status: {status}')
            image.Release()
            return None
        np_img = image.GetNDArray()
        image.Release()
        return np_img

    def get_live_stream_image(self):
        self.mode = 'live_stream'
        image = self.cam.GetNextImage()
        if image.IsIncomplete():
            status = image.GetImageStatus()
            self.log.error(f'Image incomplete, status: {status}')
            image.Release()
            return None

        n = image.GetNumChannels()
        h = image.GetHeight()
        w = image.GetWidth()
        image.Release()
        if n > 1:
            array = image.GetData().reshape(h, w, n)
        else:
            array = image.GetData().reshape(h, w).T
            array = array[..., np.newaxis].repeat(3, -1).astype("uint8")
        image.Release()

        return array

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        if m not in {None, 'capture', 'live_stream'}:
            raise KeyError(m)
        if m == self.mode:
            return
        if self.mode == 'live_stream':
            self.cam.EndAcquisition()
        self.log.debug(f'switching to mode: {m}')
        self._mode = m
        if m == 'capture':
            self.switch_to_capture_mode()
        elif m == 'live_stream':
            self.switch_to_live_stream_mode()

    def setup_basic(self):
        self.cam['StreamBufferHandlingMode'].value = 'NewestOnly'
        self.cam['GainAuto'].value = 'Off'
        self.cam['Gain'].value = 0
        self.cam['TriggerMode'].value = 'Off'
        self.cam['DecimationSelector'].value = 'All'

    def switch_to_capture_mode(self):
        if self.expo_time is None:
            raise SystemError('Exposure time is not set')
        self._set_acquisition_mode('single')
        self.setup_basic()
        self._set_res('max', 'max')
        self._set_crc_check(True)
        self._set_gain(False)
        self._set_expo_time(self.expo_time)
        self._set_pixel_format('Mono8')

    def switch_to_live_stream_mode(self):
        self._set_acquisition_mode('continuous')
        self.setup_basic()
        self._set_res(*self.live_res)
        self._set_crc_check(False)
        self._set_expo_time('auto')
        self._set_pixel_format('Mono8')
        self.cam.BeginAcquisition()

    def _set_acquisition_mode(self, m):
        if m is 'single':
            self.cam['AcquisitionMode'].value = 'SingleFrame'
        elif m is 'continuous':
            self.cam['AcquisitionMode'].value = 'Continuous'
            self.cam['AcquisitionFrameRateEnable'].value = True
            self.cam['AcquisitionFrameRate'].value = self.live_fps
        else:
            raise KeyError(m)

    def _set_pixel_format(self, pf):
        self.cam['PixelFormat'].value = pf

    def _set_res(self, w, h, binning=False):
        w = self.cam['Width'].max if w is 'max' else w
        h = self.cam['Height'].max if h is 'max' else h
        self.cam['Width'].value = w
        self.cam['Height'].value = h

        if binning:
            self.cam['BinningHorizontal'].value = 4
            self.cam['BinningVertical'].value = 4
            self.cam['BinningHorizontalMode'].value = 'Average'
            self.cam['BinningVerticalMode'].value = 'Average'
        else:
            self.cam['BinningHorizontal'].value = 1
            self.cam['BinningVertical'].value = 1

    def _set_crc_check(self, crc):
        self.cam['StreamCRCCheckEnable'].value = crc

    def _set_expo_time(self, t):
        if t is 'auto':
            self.cam['ExposureAuto'].value = 'Continuous'
            self.cam['AutoExposureExposureTimeUpperLimit'].value = self.expo_max
        else:
            self.cam['ExposureAuto'].value = 'Off'
            self.cam['ExposureTime'].value = self.expo_time

    def __del__(self):
        self.log.debug('Deletting acquisition')
        if self.mode == 'live_stream':
            self.cam.EndAcquisition()
