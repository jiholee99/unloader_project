from adapters.image_process import ImagePreprocessor, ImagePostProcessor
from adapters.config import AppConfigAdapter
from core.inspection import ImagePreprocessService, ImagePostProcessorService, InspectionService

class InspectionFactory:
    @staticmethod
    def create():
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
        return InspectionService(pre, post)
