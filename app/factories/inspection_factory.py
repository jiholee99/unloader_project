from adapters.image_process import ImagePreprocessor, ImagePostProcessor
from adapters.config import AppConfigAdapter
from core.inspection import ImagePreprocessService, ImagePostProcessorService, InspectionService

from exceptions.exception import FactoryException

from utils.logger import get_logger

logger = get_logger("Factory")

class InspectionFactory:
    @staticmethod
    def create():
        try:
            logger.info("Creating Inspection Service...")
            config = AppConfigAdapter()
            preprocessor = ImagePreprocessor()
            postprocessor = ImagePostProcessor()
            pre = ImagePreprocessService(
                preProcessor=preprocessor,
                config=config.load_preprocess(),
                roi_coords=config.load_roi()
            )
            post = ImagePostProcessorService(
                post_processor=postprocessor,
                config=config.load_postprocess()
            )
            logger.info("Inspection Service created successfully.")
            return InspectionService(pre, post)
        except Exception as e:
            raise FactoryException("Failed to create Inspection Service.", e)
