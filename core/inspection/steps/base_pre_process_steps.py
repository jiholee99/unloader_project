from exceptions.exception import InspectionStepException
from core.interfaces import InspectionStep
from adapters.image_process import ImagePreprocessor
from adapters.config import AppConfigAdapter
from adapters.image_process import ImagePreprocessor
import numpy as np
from utils.visual_debugger import show_scaled
from utils.logger import get_logger
class GrayScaleConversionStep(InspectionStep):
    def execute(self, image : any) -> np.ndarray:
        """
        Convert the given image to grayscale.
        Returns the grayscale image.
        """
        try:
            result = ImagePreprocessor.convert_to_grayscale(image)
            return result
        except Exception as e:
            raise InspectionStepException("Failed to convert image to grayscale during grayscale conversion step.", e)

class BinaryMaskGenerationStep(InspectionStep):
    def execute(self, image : any, min_threshold: int = 55, max_threshold: int = 255) -> np.ndarray:
        """
        Apply thresholding to the given grayscale image.
        Returns the binary mask.
        """
        try:
            result = ImagePreprocessor.apply_threshold(gray_image=image, min_threshold=min_threshold, max_threshold=max_threshold)
            return result
        except Exception as e:
            raise InspectionStepException("Failed to apply threshold during binary mask generation step.", e)


class CropROIGenerationStep(InspectionStep):
    def execute(self, image, roi_coords : list, use_roi_fallback: bool = True):
        """
        Crop the region of interest (ROI) from the given image based on the image type.
        """
        try:
            return ImagePreprocessor.crop_roi(image, *roi_coords)
        except Exception as e:
            if use_roi_fallback:
                # Return the original image if cropping fails and fallback is enabled
                logger = get_logger("CropROIGenerationStep")
                logger.warning("Cropping ROI failed, returning original image as fallback. (Using the full image)")
                return image
            raise InspectionStepException("Failed to crop ROI during crop ROI generation step.", e)

class RemoveBrightLineStep(InspectionStep):
    def execute(self, image, orientation: str = 'horizontal'):
        """
        Remove bright line from the given image based on the specified orientation.
        """
        try:
            return ImagePreprocessor.preprocess_remove_bright_line(img=image, orientation=orientation)
        except Exception as e:
            raise InspectionStepException("Failed to remove bright line during remove bright line step.", e)