from . import camera as cam
import cv2
import numpy as np
from logging import getLogger

#frameWidth = 640
#frameHeight = 480

#cap = cv2.VideoCapture(0)
#cap.set(3,frameWidth)
#cap.set(4, frameHeight)
#cap.set(10,150)


class Acquistion:

    def __init__(self):
        self.acq_log = getLogger('main.acquisition')
        self.cam = cam.Camera()  #cap.read() 

    def BeginAcquisition(self):
        self.cam.BeginAcquisition()

    def get_image():
        pass

    def EndAcquisition(self):
        self.cam.EndAcquisition()

    def __del__(self):
        self.acq_log.debug('in acquisition del')
        self.cam.EndAcquisition()
        self.acq_log.debug('end acq')
        self.cam.DeInit()
        self.acq_log.debug('deinit')
        self.cam.Clear_cam_list()
        self.acq_log.debug('clear cam')
        self.cam.Delete()
        self.acq_log.debug('delete fct')
        self.cam.ReleaseInstance()
        self.acq_log.debug('release of cam')
        del self.cam
        self.acq_log.debug('acquisition del')


class Capture(Acquistion):

    def __init__(self, expo_time=20000):
        super().__init__()
        self.log = getLogger('main.capture')
        self.log.debug('created capture')
        self.cam['StreamBufferHandlingMode'].value = 'NewestOnly'
        # TODO: use full depth, i.e 12 bits for image analysis :PixelFormat_Mono12p, try with packed
        self.cam['PixelFormat'].value = 'Mono8'
        self.cam['AcquisitionMode'].value = 'Continuous'
        self.cam['StreamCRCCheckEnable'].value = True
        self.cam['DecimationSelector'].value = 'All'
        self.cam['BinningHorizontal'].value = 1
        self.cam['BinningVertical'].value = 1

        #TODO give size to constructor depending on window size
        print(f'width before camSet :{self.cam["Width"].value}')
        print(f'height before camSet :{self.cam["Height"].value}')
        print(f'width before camSet :{self.cam["Width"].max}')
        print(f'height before camSet :{self.cam["Height"].max}')

        self.cam['Width'].value = self.cam['Width'].max
        self.cam['Height'].value = self.cam['Height'].max

        print(f'width after camSet :{self.cam["Width"].value}')
        print(f'height after camSet :{self.cam["Height"].value}')
        self.cam['GainAuto'].value = 'Off'
        self.cam['Gain'].value = 0
        self.cam['AutoExposureExposureTimeUpperLimit'].value = 50000
        self.cam['ExposureAuto'].value = 'Off'
        self.cam['ExposureTime'].value = expo_time
        self.BeginAcquisition()

    def get_image(self):
        image = self.cam.GetNextImage()
        self.log.debug(f'image collected {image}')
        if image.IsIncomplete():
            self.log.error('Image incomplete with image status %d...' % image.GetImageStatus())
            image.Release()
            return None

        # Convert image to Mono8
        import PySpin as spin
        image_converted = image.Convert(spin.PixelFormat_Mono8)
        return image_converted.GetNDArray()

    def get_exposure_time(self):
        self.EndAcquisition()
        self.cam['ExposureAuto'].value = 'Once'
        old_expo_time = self.cam['ExposureTime'].value
        self.BeginAcquisition()

        for i in range(50):
            image = self.cam.GetNextImage()
            if image.IsIncomplete():
                self.log.error('Image incomplete with image status %d...' % image.GetImageStatus())
                image.Release()
                return None
            #chunk_data = im.GetChunkData()

        self.EndAcquisition()
        self.cam['ExposureAuto'].value = 'Off'
        expo_time = self.cam['ExposureTime'].value
        self.cam['ExposureTime'].value = old_expo_time
        self.BeginAcquisition()
        return expo_time

class LiveStream(Acquistion):
    def __init__(self):
        super().__init__()
        self.log = getLogger('main.LiveStream')
        self.log.debug('created livestream')
        self.cam['StreamBufferHandlingMode'].value = 'NewestFirst'
        self.cam['TriggerMode'].value = 'Off'
        self.cam['AcquisitionFrameRateEnable'].value = True
        self.cam['AcquisitionFrameRate'].value = self.cam['AcquisitionFrameRate'].max
        self.cam['StreamCRCCheckEnable'].value = False
        self.cam['AcquisitionMode'].value = 'Continuous'
        self.cam['DecimationSelector'].value = 'All'
        self.cam['BinningHorizontal'].value = 4
        self.cam['BinningVertical'].value = 4
        self.cam['BinningHorizontalMode'].value = 'Average'
        self.cam['BinningVerticalMode'].value = 'Average'
        self.cam['PixelFormat'].value = 'Mono8'
        self.cam['GainAuto'].value = 'Off'
        self.cam['Gain'].value= 0
        self.cam['AutoExposureExposureTimeUpperLimit'].value = 50000
        self.cam['ExposureAuto'].value = 'Once'
        #TODO take smaller part of image if lagging
        self.cam['Width'].value = self.cam['Width'].max
        self.cam['Height'].value = self.cam['Height'].max
        self.BeginAcquisition()

    def get_image(self):
        image = self.cam.GetNextImage()
        if image.IsIncomplete():
            self.log.warning('Image incomplete with image status %d...' % image.GetImageStatus())
            image.Release()
            return None

        h = image.GetHeight()
        w = image.GetWidth()
        numChannels = image.GetNumChannels()
        if numChannels > 1:
            array = image.GetData().reshape(h, w, numChannels)
        else:
            array = image.GetData().reshape(h, w).T
            array = array[..., np.newaxis].repeat(3, -1).astype("uint8")
        image.Release()

        return array
