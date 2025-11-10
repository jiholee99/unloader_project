import cv2
import numpy as np
from exceptions.exception import DistanceValidationException
from utils.logger import get_logger

class FullnessValidator:
    """
    Validator used to see if the roller is in valid distance range.
    """
    def _calculate_fullness(self, preprocessed_image, threshold: int) -> float:
        """
        Calculate how full the roller is in the image.
        Args:
            preprocessed_image: The preprocessed image to analyze.
            roi: The region of interest (ROI) to consider for fullness calculation.
            threshold: The fullness threshold.
        Returns:
            float: A value representing how full the roller is.
        """
        try:
            total_pixels = preprocessed_image.size
            if total_pixels == 0:
                return 0.0
            filled_pixels = cv2.countNonZero((preprocessed_image < threshold).astype(np.uint8))
            fullness = filled_pixels / total_pixels
            get_logger().info(f"Calculated fullness: {fullness * 100:.4f}%")
            return fullness
        except Exception as e:
            raise DistanceValidationException(f"Error calculating fullness: {e}",e)

    def is_valid(self, preprocessed_image, threshold: int, cutoff_point: float) -> bool:
        """
        Takes in a preprocessed image and determines if the roller is within valid distance range.
        Args:
            preprocessed_image: The preprocessed image to analyze.
            roi: The region of interest (ROI) to consider for validation.
            threshold: The fullness threshold.
            cutoff_point: The cutoff point for determining validity.
        Returns:
            bool: True if the roller is within valid distance range, False otherwise.
        """
        try:
            fullness = self._calculate_fullness(preprocessed_image,threshold)
            return fullness >= cutoff_point
        except Exception as e:
            raise DistanceValidationException(original_exception=e)
