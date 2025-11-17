from adapters.image_process import ImagePostProcessor, ContourProcessor
from exceptions.exception import ImagePostProcessingException
from utils.logger import get_logger


class ImagePostProcessorService:
    """
    Service layer for image post-processing tasks.
    Uses ImagePostProcessor to perform operations.
    """

    def __init__(self, post_processor : ImagePostProcessor, config: dict = {}):
        self.post_processor = post_processor
        self._contours = None
        self._config = config
        self.logger = get_logger(__name__)

    def post_process(self, mask):
        try:
            if self._config.get("use_fill_holes", False):
                mask = self.post_processor.fill_holes_in_mask(mask)
            contours = self.post_processor.detect_contours(mask)
            self._contours = contours
            return mask
        except Exception as e:
            raise ImagePostProcessingException(f"Post-processing Service error", e)

    def get_contours(self):
        return self._contours

    def log_contour_info(self):
        if not self._contours:
            self.logger.warning("No contours available to log.")
            return
        i = 1
        self.logger.info(f"Total contours detected: {len(self._contours)}")
        for contour in self._contours:
            info = ContourProcessor.get_contour_info(contour)
            self.logger.info(
                f"""
                Contour {i}
                    - Area: {info['area']:.4f}
                    - Perimeter: {info['perimeter']:.4f}
                    - Bounding Box: {info['bounding_box']}
                    - Aspect Ratio: {info['aspect_ratio']:.4f}
                    - Extent: {info['extent']:.4f}
                    - Solidity: {info['solidity']:.4f}
                """
            )
            i += 1
