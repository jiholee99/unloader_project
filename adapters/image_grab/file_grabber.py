import cv2
from exceptions.exception import ImageGrabException
from core.interfaces import Grabber
import numpy as np

class FileGrabber(Grabber):
    def __init__(self, config: dict = None):
        self.config = config

    def init_grabber(self):
        return

    def grab_image(self) -> np.ndarray:
        image_path = self.config.get("image_path") if self.config else None
        if not image_path:
            raise ImageGrabException("Image path not provided for FileGrabber.")
        image = cv2.imread(image_path)
        if image is None:
            raise ImageGrabException(f"Failed to load image from path: {image_path}")
        return image

    def close(self) -> None:
        return
    
    def change_image_path(self, new_path: str) -> None:
        if not self.config:
            self.config = {}
        self.config["image_path"] = new_path