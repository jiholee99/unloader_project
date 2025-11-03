import cv2
from exceptions.exception import ImageProcessingException
import numpy as np
class ImagePreprocessor:
    def convert_to_grayscale(self, image):
        """Convert the input image to grayscale."""
        try:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            raise ImageProcessingException(f"Error converting image to grayscale",e)
        
    def crop_roi(self, image, x, y, w, h):
        """Crop the region of interest from the image. Returns the cropped image."""
        try:
            roi = image[y:y+h, x:x+w]
            if roi.size == 0:
                raise ImageProcessingException("Cropped ROI is empty or out of bounds.")
            return roi
        except Exception as e:
            raise ImageProcessingException(f"Error cropping ROI",e)

    def apply_threshold(self, gray_image, min_threshold, max_threshold = 255):
        """Apply binary thresholding to the grayscale image."""
        try:
            _, mask = cv2.threshold(gray_image, min_threshold, max_threshold, cv2.THRESH_BINARY)
            return mask
        except Exception as e:
            raise ImageProcessingException(f"Error applying threshold",e)

    def detect_contours(self, mask_image, min_area = 30000):
        """Detect contours in the binary mask image."""
        try:
            mask = cv2.bitwise_not(mask_image)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
            return valid_contours
        except Exception as e:
            raise ImageProcessingException(f"Error detecting contours",e)
        
    
    def fill_holes_in_mask(self, mask):
        """Fill small holes inside white regions of a binary mask."""
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
    
    def merge_close_regions(self, mask, kernel_size=(15, 15)):
        """Merge nearby contours in a binary mask using morphological closing."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        merged_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return merged_mask

    def merge_nearby_contours(self,contours, distance_threshold=50):
        """
        Merge contours that are horizontally or vertically close to each other.
        Args:
            contours (list): list of contours from cv2.findContours
            distance_threshold (int): max pixel distance between contours to merge
        Returns:
            list: merged contours
        """
        if not contours:
            return []

        merged_contours = []
        used = set()

        for i, c1 in enumerate(contours):
            if i in used:
                continue

            x1, y1, w1, h1 = cv2.boundingRect(c1)
            merged_mask = np.zeros((h1 + distance_threshold*2, w1 + distance_threshold*2), np.uint8)
            cv2.drawContours(merged_mask, [c1 - [x1 - distance_threshold, y1 - distance_threshold]], -1, 255, -1)

            for j, c2 in enumerate(contours):
                if j == i or j in used:
                    continue
                x2, y2, w2, h2 = cv2.boundingRect(c2)
                # Check if they overlap or are close horizontally/vertically
                if (abs(x1 - x2) < distance_threshold or abs(y1 - y2) < distance_threshold):
                    cv2.drawContours(merged_mask, [c2 - [x1 - distance_threshold, y1 - distance_threshold]], -1, 255, -1)
                    used.add(j)

            # Recalculate contour from merged mask
            merged_contour, _ = cv2.findContours(merged_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            merged_contours.extend(merged_contour)
            used.add(i)

        return merged_contours

    