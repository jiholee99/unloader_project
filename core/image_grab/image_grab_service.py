import numpy as np
from exceptions.exception import ImageGrabException
from adapters.image_grab import CameraGrabber, CameraGrabber
from core.interfaces import Grabber

class ImageGrabService:
    def __init__(self, grabber : Grabber):
        self.grabber = grabber
        self.grabber.init_grabber()
    
    def grab_image(self) -> np.ndarray:
        return self.grabber.grab_image()
    
    def close_grabber(self):
        return self.grabber.close()