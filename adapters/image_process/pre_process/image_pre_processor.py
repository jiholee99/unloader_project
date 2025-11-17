import cv2
from exceptions.exception import ImagePreProcessorException
import numpy as np
class ImagePreprocessor:
    @staticmethod
    def convert_to_grayscale(image):
        """Convert the input image to grayscale."""
        try:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            raise ImagePreProcessorException(f"Error converting image to grayscale",e)
    @staticmethod    
    def crop_roi(image, x, y, w, h):
        """Crop the region of interest from the image. Returns the cropped image."""
        try:
            roi = image[y:y+h, x:x+w]
            if roi.size == 0:
                raise ImagePreProcessorException("Cropped ROI is empty or out of bounds.")
            return roi
        except Exception as e:
            raise ImagePreProcessorException(f"Error cropping ROI",e)
    @staticmethod
    def apply_threshold(gray_image, min_threshold, max_threshold = 255):
        """Apply binary thresholding to the grayscale image."""
        try:
            _, mask = cv2.threshold(gray_image, min_threshold, max_threshold, cv2.THRESH_BINARY)
            return mask
        except Exception as e:
            raise ImagePreProcessorException(f"Error applying threshold",e)
    @staticmethod
    def preprocess_remove_bright_line(img, orientation='vertical'):
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 1: Detect pure white or near-white pixels
        # Add small blur to connect broken parts of the streak
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        mask = cv2.inRange(blur, 240, 255)

        # Step 2: Strengthen the mask to cover the entire line
        if orientation == 'vertical':
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
        else:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 9))
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Step 3: Inpaint to remove the line intelligently
        cleaned = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)

        return cleaned


    