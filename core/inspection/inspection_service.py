import cv2
#Exceptions
from exceptions.exception import InspectionException
# Core Services
from core.inspection.image_process import ImagePreprocessService, ImagePostProcessorService

import numpy as np

# Utils
from utils.logger import get_logger
from utils.visual_debugger import show_scaled

class InspectionService:
    def __init__(self, pre_processor : ImagePreprocessService, post_processor : ImagePostProcessorService):
        self.logger = get_logger()

        self._pre_processor = pre_processor
        self._post_processor = post_processor
        self._pre_mask_image = None
        self._post_mask_image = None
        self._contours = []


    def _is_roller(self):
        pass

    def _is_close(self):
        pass

    def get_pre_processed_image(self):
        return self._pre_mask_image
    
    def get_post_processed_image(self):
        return self._post_mask_image
    
    def get_contours(self):
        return self._post_processor.get_contours()

    def inspect(self, image : np.ndarray):
        try:
            show_scaled("Original Image", image)
            self._pre_mask_image = self._pre_processor.process_image(image=image)
            self._post_mask_image = self._post_processor.post_process(self._pre_mask_image)
            self._contours = self._post_processor.get_contours()

            # Debug visualization
            show_scaled(f"Pre-Processed Image", self._pre_mask_image)
            show_scaled(f"Post-Processed Mask", self._post_mask_image,)
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            roller_status = self._is_roller()
            close_status = self._is_close()
        except Exception as e:
            raise InspectionException("Inspection process error occurred.", e)
        

        pass


if __name__ == "__main__":
    # service = InspectionService()
    # service.inspect()
    print("Inspection Service Module")