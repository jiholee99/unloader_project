import cv2
from exceptions.exception import ImageGrabException
import numpy as np

class CameraGrabber():
    @staticmethod
    def grab_image(config: dict) -> np.ndarray:
        # Implementation for grabbing an image from a camera
        capture = cv2.VideoCapture(config.get("camera_index", 0))

        if not capture.isOpened():
            raise ImageGrabException("Failed to open camera.")
        
        ret, frame = capture.read()
        capture.release()

        if not ret:
            raise ImageGrabException("Failed to grab image from camera.")
        
        return frame