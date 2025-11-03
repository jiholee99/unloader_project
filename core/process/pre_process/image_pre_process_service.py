from core.process.pre_process.image_pre_processor import ImagePreprocessor
from exceptions.exception import ImageProcessingException

class ImagePreprocessService:
    # Swap out the preprocessor for easier testing/mocking
    def __init__(self, preProcessor = ImagePreprocessor()):
        self.preprocessor = preProcessor
        self._roi_image = None

    def process_image(self, image, roi_coords : list[int], threshold: int, max_threshold = 255):
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
            self._roi_image = self.preprocessor.crop_roi(image, *roi_coords)
            gray = self.preprocessor.convert_to_grayscale(self._roi_image)
            mask = self.preprocessor.apply_threshold(gray, threshold, max_threshold)
            return mask
        except Exception as e:
            raise ImageProcessingException(f"Image processing service error",e)
        

    def get_roi_image(self):
        return self._roi_image