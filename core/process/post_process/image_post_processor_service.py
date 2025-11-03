from core.process.post_process.image_post_processor import ImagePostProcessor
from exceptions.exception import ImagePostProcessingException

class ImagePostProcessorService:
    """
    Service layer for image post-processing tasks.
    Uses ImagePostProcessor to perform operations.
    """
    def __init__(self, post_processor = ImagePostProcessor()):
        self.post_processor = post_processor
        self._contours = None

    def post_process(self, mask):
        try:
            filled_mask = self.post_processor.fill_holes_in_mask(mask)
            contours = self.post_processor.detect_contours(filled_mask)
            self._contours = contours
            return filled_mask
        except Exception as e:
            raise ImagePostProcessingException(f"Post-processing error", e)
        
    def get_contours(self):
        return self._contours
