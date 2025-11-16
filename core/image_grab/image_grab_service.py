import numpy as np
from exceptions.exception import ImageGrabException

from core.image_grab.file_grabber import FileGrabber
from core.image_grab.camera_grabber import CameraGrabber

class ImageGrabService:
    @staticmethod
    def grab_image_from_camera(config: dict = {}) -> np.ndarray:
        try:
            return CameraGrabber.grab_image(config)
        except Exception as e:
            raise ImageGrabException("Failed to grab image from camera.", e)
    
    @staticmethod
    def grab_image_from_file(image_path: str) -> np.ndarray:
        try:
            return FileGrabber.grab_image_from_file(image_path)
        except Exception as e:
            raise ImageGrabException("Failed to grab image from file.", e)
    
    @staticmethod
    def grab_multiple_images_from_files(image_paths: list) -> list:
        try:
            return FileGrabber.grab_multiple_images_from_files(image_paths)
        except Exception as e:
            raise ImageGrabException("Failed to grab multiple images from files.", e)