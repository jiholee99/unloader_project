import cv2
from exceptions.exception import ImageGrabException
import numpy as np

class FileGrabber():
    @staticmethod
    def grab_image_from_file(image_path: str) -> np.ndarray:
        """
        Grabs an image from a file based on the provided file path.
        Args:
            image_path (str): Path to the image file.
        Returns:
            np.ndarray: Loaded image as a BGR numpy array.
        """
        if not image_path:
            raise ImageGrabException("Image path not provided for FileGrabber.")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ImageGrabException(f"Failed to load image from path: {image_path}")
        
        return image
    
    @staticmethod
    def grab_multiple_images_from_files(image_paths: list) -> list:
        """
        Grabs multiple images from a list of file paths.
        Args:
            image_paths (list): List of image file paths.
        Returns:
            list: List of loaded images as BGR numpy arrays.
        """
        if not image_paths:
            raise ImageGrabException("Image paths not provided for FileGrabber.")
        
        images = []
        for path in image_paths:
            image = FileGrabber.grab_image_from_file(path)
            images.append(image)
        
        return images