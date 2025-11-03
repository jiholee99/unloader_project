import cv2
import numpy as np

class ImageModel:
    """Handles all image data and OpenCV processing logic."""

    def __init__(self):
        self.image = None
        self.processed_image = None

    def load_image(self, path: str):
        self.image = cv2.imread(path)
        if self.image is None:
            raise FileNotFoundError("Could not load image.")
        return self.image

    def apply_threshold(self, threshold=128):
        if self.image is None:
            raise ValueError("No image loaded.")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        self.processed_image = mask
        return self.processed_image
