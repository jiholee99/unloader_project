import cv2
import numpy as np

from exceptions.exception import ImagePostProcessingException

class ImagePostProcessor:
    @staticmethod
    def detect_contours(mask_image, min_area = 50000):
        """Detect contours in the binary mask image."""
        try:
            mask = cv2.bitwise_not(mask_image)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
            return valid_contours
        except Exception as e:
            raise ImagePostProcessingException(f"Error detecting contours",e)

    @staticmethod
    def fill_holes_in_mask(mask):
        """Fill small holes inside white regions of a binary mask."""
        try:
            mask = cv2.bitwise_not(mask)  # invert so object is white
            mask = (mask > 0).astype(np.uint8) * 255

            h, w = mask.shape[:2]
            floodfill_mask = np.zeros((h + 2, w + 2), np.uint8)
            floodfilled = mask.copy()
            cv2.floodFill(floodfilled, floodfill_mask, (0, 0), 255)

            floodfilled_inv = cv2.bitwise_not(floodfilled)
            filled_mask = mask | floodfilled_inv
            filled_mask = cv2.bitwise_not(filled_mask)  # invert back to original polarity
            return filled_mask
        except Exception as e:
            raise ImagePostProcessingException(f"Error filling holes in mask",e)
