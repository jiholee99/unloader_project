from core.process.post_process.image_post_processor import ImagePostProcessor
from core.process.post_process.contour_processor import ContourProcessor
from exceptions.exception import ImagePostProcessingException
from utils.logger import get_logger

class ImagePostProcessorService:
    """
    Service layer for image post-processing tasks.
    Uses ImagePostProcessor to perform operations.
    """
    def __init__(self, post_processor = ImagePostProcessor(), options: dict = {}):
        self.post_processor = post_processor
        self._contours = None
        self._options = options
        self.logger = get_logger(__name__)

    def post_process(self, mask):
        try:
            if self._options.get("use_fill_holes", False):
                mask = self.post_processor.fill_holes_in_mask(mask)
            contours = self.post_processor.detect_contours(mask)
            self.logger.info(f"Detected {len(contours)} contours after post-processing.")
            for contour in contours:
                self.logger.info(f"Contour info {ContourProcessor.get_contour_info(contour)}")
                self.logger.info(f"Detected contour is square`: {self.post_processor.is_contour_square(contour)}")
            self._contours = contours
            return mask
        except Exception as e:
            raise ImagePostProcessingException(f"Post-processing error", e)
        
    def get_contours(self):
        return self._contours
