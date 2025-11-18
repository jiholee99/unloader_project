import cv2
import numpy as np
from exceptions.exception import ImageGrabException
from core.interfaces import Grabber


class CameraGrabber(Grabber):
    def __init__(self, config: dict = {}):
        self.capture = None
        self.config = config

    def __del__(self):
        print("Releasing camera resources...")
        self.close()

    def init_grabber(self):
        """ Initialize the camera once. """
        camera_index = self.config.get("camera_index", 0)
        self.capture = cv2.VideoCapture(camera_index)

        if not self.capture.isOpened():
            raise ImageGrabException(f"Failed to open camera at index {camera_index}")

    def grab_image(self) -> np.ndarray:
        """ Grab a frame without reopening camera. """
        if self.capture is None:
            raise ImageGrabException("Camera has not been initialized. Call init_grabber() first.")

        ret, frame = self.capture.read()

        if not ret:
            raise ImageGrabException("Failed to grab image from camera.")

        return frame

    def close(self):
        """ Release the camera gracefully. """
        if self.capture is not None:
            self.capture.release()
            self.capture = None
