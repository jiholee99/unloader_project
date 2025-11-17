from core.inspection.process.pre_process.image_pre_processor import ImagePreprocessor
from exceptions.exception import ImagePreProcessServiceException
from utils.logger import get_logger

class ImagePreprocessService:
    # Swap out the preprocessor for easier testing/mocking
    def __init__(self, preProcessor = ImagePreprocessor(), options: dict = {} ):
        self.preprocessor = preProcessor
        self._roi_image = None
        self._options = options
        self.logger = get_logger(__name__)

    def process_image(self, image, roi_coords : list[int], threshold: int = 0, max_threshold = 255):
        """
        Process the image through various stages.\n
        Right now includes grayscale conversion, ROI cropping, and thresholding.
        Args:
            image: Input image in BGR format.
            roi_coords: List of ROI coordinates [x, y, w, h].
            threshold: Minimum threshold value for binary thresholding.
            max_threshold: Maximum threshold value for binary thresholding.
        Returns:
            mask: The binary mask after thresholding the cropped ROI.
        """
        try:
            # Essential steps. Do not use options to disable these.
            self._roi_image = self.preprocessor.crop_roi(image, *roi_coords,)
            preprocessed_mask_img = self._roi_image
            # Optional: Remove bright line if enabled
            if self._options.get("use_remove_bright_line", False):
                preprocessed_mask_img = self.preprocessor.preprocess_remove_bright_line(img=self._roi_image, orientation='horizontal')
            else:
                preprocessed_mask_img = self._roi_image
            
            gray = self.preprocessor.convert_to_grayscale(preprocessed_mask_img)
            mask = self.preprocessor.apply_threshold(gray, self._options.get("threshold", threshold), max_threshold)
            return mask
        except Exception as e:
            raise ImagePreProcessServiceException(f"Image processing service error",e)
        
    def get_options(self):
        return self._options
    
    def get_roi_image(self):
        return self._roi_image